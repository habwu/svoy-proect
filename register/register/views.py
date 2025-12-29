from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from register.models import Register, RegisterSend, RegisterAdmin, Recommendation
from .serializers import (
    RegisterSerializer,
    RegisterSendSerializer,
    RegisterAdminSerializer,
    RecommendationSerializer,
)


class RegisterViewSet(ModelViewSet):
    """
    ViewSet для управления заявками (Register).
    """

    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def student_registers(self, request):
        """
        Получение заявок текущего ученика.
        """
        registers = Register.objects.filter(child=request.user)
        serializer = self.get_serializer(registers, many=True)
        return Response(serializer.data)


class RegisterSendViewSet(ModelViewSet):
    """
    ViewSet для управления отправленными заявками (RegisterSend).
    """

    queryset = RegisterSend.objects.all()
    serializer_class = RegisterSendSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def teacher_registers(self, request):
        """
        Получение заявок, отправленных текущим учителем.
        """
        registers = RegisterSend.objects.filter(teacher_send=request.user)
        serializer = self.get_serializer(registers, many=True)
        return Response(serializer.data)


class RegisterAdminViewSet(ModelViewSet):
    """
    ViewSet для управления заявками администраторов (RegisterAdmin).
    """

    queryset = RegisterAdmin.objects.all()
    serializer_class = RegisterAdminSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def admin_registers(self, request):
        """
        Получение заявок, утвержденных администратором.
        """
        registers = RegisterAdmin.objects.filter(teacher_admin=request.user)
        serializer = self.get_serializer(registers, many=True)
        return Response(serializer.data)


class RecommendationViewSet(ModelViewSet):
    """
    ViewSet для управления рекомендациями (Recommendation).
    """

    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def accept(self, request, pk=None):
        """
        Принятие рекомендации учеником.
        """
        recommendation = get_object_or_404(Recommendation, pk=pk, recommended_to=request.user)
        recommendation.status = Recommendation.ACCEPTED
        recommendation.save()
        return Response({"detail": "Рекомендация принята."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def decline(self, request, pk=None):
        """
        Отклонение рекомендации учеником.
        """
        recommendation = get_object_or_404(Recommendation, pk=pk, recommended_to=request.user)
        recommendation.status = Recommendation.DECLINED
        recommendation.save()
        return Response({"detail": "Рекомендация отклонена."}, status=status.HTTP_200_OK)
