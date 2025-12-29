from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import School
from manager.models import SchoolApplication
from .serializers import SchoolSerializer, SchoolApplicationSerializer


class SchoolViewSet(ModelViewSet):
    """
    ViewSet для управления школами.
    """

    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает школы, связанные с пользователями или все школы для администратора.
        """
        user = self.request.user
        if user.is_admin:
            return School.objects.all()
        return School.objects.filter(admin_user=user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_school(self, request):
        """
        Возвращает школу, которой управляет текущий пользователь.
        """
        user = request.user
        school = School.objects.filter(admin_user=user).first()
        if not school:
            return Response({"detail": "Вы не являетесь администратором какой-либо школы."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(school)
        return Response(serializer.data)


class SchoolApplicationViewSet(ModelViewSet):
    """
    ViewSet для управления заявками на регистрацию школ.
    """
    queryset = SchoolApplication.objects.all()
    serializer_class = SchoolApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Устанавливает статус "В ожидании" при создании заявки.
        """
        serializer.save(status='pending')
