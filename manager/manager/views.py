from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import SchoolApplication
from .serializers import SchoolApplicationSerializer


class SchoolApplicationViewSet(ModelViewSet):
    """
    ViewSet для управления заявками на регистрацию школ.
    """
    queryset = SchoolApplication.objects.all()
    serializer_class = SchoolApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Определение прав доступа для различных действий.
        """
        if self.action in ['approve_application', 'reject_application']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve_application(self, request, pk=None):
        """
        Подтверждение заявки на регистрацию школы.
        """
        application = self.get_object()
        if application.status == 'approved':
            return Response({'detail': 'Заявка уже подтверждена.'}, status=status.HTTP_400_BAD_REQUEST)

        application.status = 'approved'
        application.school_created = True
        application.save()

        return Response({'detail': 'Заявка успешно подтверждена.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject_application(self, request, pk=None):
        """
        Отклонение заявки на регистрацию школы.
        """
        application = self.get_object()
        if application.status == 'rejected':
            return Response({'detail': 'Заявка уже отклонена.'}, status=status.HTTP_400_BAD_REQUEST)

        application.status = 'rejected'
        application.save()

        return Response({'detail': 'Заявка успешно отклонена.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def send_credentials(self, request, pk=None):
        """
        Отправка учетных данных заявителю.
        """
        application = self.get_object()
        if not application.school_created:
            return Response({'detail': 'Сначала нужно создать школу.'}, status=status.HTTP_400_BAD_REQUEST)

        # Логика отправки учетных данных (например, по email)
        # Здесь можно добавить вызов внешнего сервиса или отправку email.

        application.credentials_sent = True
        application.save()

        return Response({'detail': 'Учётные данные успешно отправлены.'}, status=status.HTTP_200_OK)
