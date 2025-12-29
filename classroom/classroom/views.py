from django.http import JsonResponse
from requests import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from users.models import User
from classroom.models import Classroom
from .serializers import (
    UserSerializer,
    ClassroomSerializer,
    PromoteAllClassroomsSerializer,
    ChangePasswordSerializer,
    ExpelStudentSerializer,
    StudentPasswordResetSerializer
)
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAdminUser
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
import secrets
import string


class UserViewSet(viewsets.ViewSet):
    """ViewSet для управления учениками."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return User.objects.filter(school=user.school, is_child=True)
        elif user.is_teacher:
            return User.objects.filter(school=user.school, is_child=True, classroom__teacher=user)
        return User.objects.none()

    def preform_create(self, serializer):
        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        serializer.save(
            school=self.request.user.school,
            is_child=True,
            password=password,
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def expel(self, request, pk=None):
        """Исключение/восстановление ученика."""
        user = get_object_or_404(User, pk=pk)
        serializer = ExpelStudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.is_expelled = serializer.validated_data.get('is_expelled')
        user.save()
        status_message = "Исключен" if user.is_expelled else "Восстановлен"
        return JsonResponse({
            "message": f"Ученик {status_message}."
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        """Изменение пароля ученику."""
        user = get_object_or_404(User, pk=pk)
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()
        return JsonResponse({
            "message": "Пароль успешно изменен."
        }, status=status.HTTP_200_OK)


class ClassroomViewSet(viewsets.ViewSet):
    """ViewSet для управления классами."""
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        graduate_param = self.request.query_params.get('graduated', '0')
        graduated = graduate_param == '1'

        if user.is_teacher or user.is_admin:
            return Classroom.objects.filter(school=user.school, is_graduated=graduated)
        return Classroom.objects.none()

    def preform_create(self, serializer):
        serializer.save(school=self.request.user.school)

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def promote_all(self, request):
        """Продвижение всех классов на следующий уровень."""
        serializer = PromoteAllClassroomsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirm = serializer.validated_data.get('confirm', False)
        if confirm:
            classrooms = Classroom.objects.filter(is_graduated=False, school=request.user.school)
            for classroom in classrooms:
                classroom.promote()
            return JsonResponse({"message": "Все классы успешно продвинуты"}, status=status.HTTP_200_OK)
        return JsonResponse({"error": "Подтверждение не получено"}, status=status.HTTP_400_BAD_REQUEST)
