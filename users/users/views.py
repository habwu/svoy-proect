from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, CreateUserSerializer, ProfileSerializer
from .models import User
from main.permissions import IsManagerUser, IsAdminUser
from result.models import Result
from raiting_system.models import Medal, Rating
from classroom.models import Classroom
import uuid


class UserViewSet(ModelViewSet):
    """ViewSet для управления пользователями."""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'create_teacher', 'create_child', 'create_admin']:
            return CreateUserSerializer
        if self.action == 'profile':
            return ProfileSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_manager:
            return User.objects.filter(school=self.request.user.school)
        return User.objects.none()

    @action(detail=True, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def profile(self, request, pk=None):
        """Просмотр или редактирование профиля пользователя."""
        user = get_object_or_404(User, pk=pk)
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def create_teacher(self, request):
        """Создание учителя."""
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save(is_teacher=True, school=request.user.school)
        return Response(UserSerializer(teacher).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def create_child(self, request):
        """Создание ученика."""
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        child = serializer.save(is_child=True, school=request.user.school)
        return Response(UserSerializer(child).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def create_admin(self, request):
        """Создание администратора."""
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin = serializer.save(is_admin=True, school=request.user.school)
        return Response(UserSerializer(admin).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        """Изменение пароля."""
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            return Response({"detail": "Нет прав на изменение пароля этого пользователя."},
                            status=status.HTTP_403_FORBIDDEN)
        user.set_password(request.data['password'])
        user.save()
        return Response({"detail": "Пароль успешно изменен."})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def teachers(self, request):
        """Список учителей текущей школы."""
        teachers = User.objects.filter(is_teacher=True, school=request.user.school)
        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def admins(self, request):
        """ Список всех администраторов школы"""
        admins = User.objects.filter(is_admin=True, school=request.user.school)
        serializer = self.get_serializer(admins, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def link_telegram(self, request, pk=None):
        """ Привязка Telegram к профилю пользователя"""
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            return Response({"detail": "Нет прав на изменение этого пользователя."}, status=status.HTTP_403_FORBIDDEN)
        link_code = uuid.uuid4().hex
        user.telegram_link_code = link_code
        user.save()
        return Response({"telegram_link_code": link_code})

    @action(detail=True, methods=['delete'], permission_classes=[IsAdminUser])
    def delete_user(self, request, pk=None):
        """Удаление пользователя."""
        user = get_object_or_404(User, pk=pk, school=request.user.school)
        user.delete()
        return Response({"detail": "Пользователь успешно удален."}, status=status.HTTP_204_NO_CONTENT)
