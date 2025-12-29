import io
import pandas as pd
from django.http import HttpResponse, Http404
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Result
from .serializers import ResultSerializer
from main.models import Olympiad
from users.models import User
from classroom.models import Classroom
from school.models import School
from raiting_system.models import Rating, Medal
import requests
from asgiref.sync import async_to_sync


class ResultViewSet(ModelViewSet):
    """
    ViewSet для управления результатами олимпиад.
    """
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает результаты, связанные с текущей школой пользователя.
        """
        if self.request.user.is_admin:
            return Result.objects.filter(school=self.request.user.school)
        return Result.objects.none()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def export_results(self, request):
        """
        Экспорт результатов в Excel файл.
        """
        results = self.get_queryset().select_related('info_children__classroom', 'info_olympiad')
        data = [
            {
                'ФИО': result.info_children.get_full_name(),
                'Класс': f"{result.info_children.classroom.number} {result.info_children.classroom.letter}" if result.info_children.classroom else 'Нет данных',
                'Название олимпиады': result.info_olympiad.name,
                'Очки': result.points,
                'Статус': result.get_status_result_display(),
                'Дата': result.date_added.strftime('%Y-%m-%d') if result.date_added else 'Нет данных',
            }
            for result in results
        ]

        df = pd.DataFrame(data)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Results')

        buffer.seek(0)
        response = HttpResponse(
            buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=results.xlsx'
        return response

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def import_results(self, request):
        """
        Импорт результатов из Excel файла.
        """
        file = request.FILES.get('file')
        if not file:
            return Response({"detail": "Файл не найден."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)
            required_columns = ['Фамилия', 'Имя', 'Отчество', 'Олимпиада', 'Очки', 'Статус']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                return Response(
                    {"detail": f"Отсутствуют столбцы: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            school = request.user.school
            for _, row in df.iterrows():
                last_name, first_name, surname = row['Фамилия'], row['Имя'], row['Отчество']
                olympiad_name, points, status = row['Олимпиада'], row['Очки'], row['Статус']

                child = User.objects.filter(
                    last_name__iexact=last_name,
                    first_name__iexact=first_name,
                    surname__iexact=surname,
                    school=school
                ).first()
                if not child:
                    continue

                olympiad = Olympiad.objects.filter(name__iexact=olympiad_name).first()
                if not olympiad:
                    continue

                Result.objects.update_or_create(
                    info_children=child,
                    info_olympiad=olympiad,
                    defaults={
                        'points': points,
                        'status_result': status,
                        'school': school
                    }
                )

            return Response({"detail": "Результаты успешно импортированы."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def send_telegram_notification(self, request, pk=None):
        """
        Отправка уведомления в Telegram.
        """
        result = self.get_object()
        student = result.info_children

        if not student.telegram_id:
            return Response({"detail": "Telegram ID не найден."}, status=status.HTTP_400_BAD_REQUEST)

        message = (
            f"👋 Здравствуйте, {student.get_full_name()}!\n\n"
            f"🎓 Результат по олимпиаде: {result.info_olympiad.name}\n"
            f"✨ Статус: {result.get_status_result_display()}\n"
            f"🏆 Очки: {result.points}"
        )

        try:
            async_to_sync(send_message_via_telegram)(student.telegram_id, message)
            return Response({"detail": "Уведомление успешно отправлено."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def send_message_via_telegram(chat_id, message):
    """
    Отправка сообщения в Telegram.
    """
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
    response = requests.post(url, data=payload)
    if not response.ok:
        raise Exception(f"Ошибка отправки сообщения: {response.text}")
