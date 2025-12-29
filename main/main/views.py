from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db.models.functions import Lower
from .models import AuditLog, Olympiad
from .serializers import (
    AuditLogSerializer,
    OlympiadSerializer,
    CreateOlympiadSerializer,
    UpdateOlympiadSerializer,
    HomePageSerializer
)
from users.models import User
from register.models import RegisterAdmin, RegisterSend
from result.models import Result
from raiting_system.models import Rating, Medal, PersonalMedal


class OlympiadViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления олимпиадами.
    """
    queryset = Olympiad.objects.all()
    serializer_class = OlympiadSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateOlympiadSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateOlympiadSerializer
        return OlympiadSerializer

    def list(self, request, *args, **kwargs):
        """
        Получение списка олимпиад с фильтрацией.
        """
        query_params = request.query_params
        query = query_params.get('query', '').strip().lower()
        date = query_params.get('date')
        category = query_params.get('category')
        stage = query_params.get('stage')
        level = query_params.get('level')
        subject = query_params.get('subject')
        class_olympiad = query_params.get('class_olympiad')
        location = query_params.get('location', '').strip().lower()

        queryset = self.queryset.annotate(
            name_lower=Lower('name'),
            category_lower=Lower('category__name'),
            stage_lower=Lower('stage__name'),
            level_lower=Lower('level__name'),
            subject_lower=Lower('subject__name'),
            location_lower=Lower('location'),
        )

        if query:
            queryset = queryset.filter(
                Q(name_lower__icontains=query) |
                Q(category_lower__icontains=query) |
                Q(stage_lower__icontains=query) |
                Q(level_lower__icontains=query) |
                Q(subject_lower__icontains=query) |
                Q(location_lower__icontains=query)
            )
        if date:
            queryset = queryset.filter(date=date)
        if category:
            queryset = queryset.filter(category_id=category)
        if stage:
            queryset = queryset.filter(stage_id=stage)
        if level:
            queryset = queryset.filter(level_id=level)
        if subject:
            queryset = queryset.filter(subject_id=subject)
        if class_olympiad:
            queryset = queryset.filter(class_olympiad=class_olympiad)
        if location:
            queryset = queryset.filter(location_lower__icontains=location)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def audit_logs(self, request):
        """
        Экшен для получения журнала аудита.
        """
        if not request.user.is_admin:
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset = AuditLog.objects.all().order_by('-timestamp')
        serializer = AuditLogSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def homepage(self, request):
        """
        Экшен для данных главной страницы.
        """
        user = request.user
        data = {
            'user_info': HomePageSerializer(user).data,
        }

        # Добавить информацию на основе роли пользователя
        if user.is_child:
            recent_results = Result.objects.filter(info_children=user, school=user.school).order_by('-date_added')[:10]
            user_rating = Rating.objects.filter(user=user).first()
            medals = Medal.objects.filter(user=user)
            personal_medals = PersonalMedal.objects.filter(user=user)
            data.update({
                'recent_results': recent_results.values(),
                'user_rating': user_rating.points if user_rating else 0,
                'medals': medals.values(),
                'personal_medals': personal_medals.values(),
            })

        elif user.is_teacher:
            classroom_students = User.objects.filter(classroom=user.classroom_guide)
            pending_applications = RegisterSend.objects.filter(teacher_send=user)
            data.update({
                'classroom_students': classroom_students.values(),
                'pending_applications': pending_applications.values(),
            })

        elif user.is_admin:
            data.update({
                'total_users': User.objects.count(),
                'total_olympiads': Olympiad.objects.count(),
                'total_applications': RegisterAdmin.objects.count(),
            })

        return Response(data)
