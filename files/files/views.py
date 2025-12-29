from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from files.models import *
from files.serializers import *

class PDFTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления папками
    """
    queryset = PDFTemplate.objects.all()
    serializer_class = PDFTemplateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Определение пользователя, который обновляет шаблоны
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='search', url_name='search')
    def search_templates(self, request):
        query = request.query_params.get('query', '')
        templates = self.get_queryset().filter(name__icontains=query)
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='preview', url_name='preview')
    def preview_template(self, request, pk=None):
        """
        Предпросмотр шаблона
        """
        template = self.get_object()
        return Response({
            "name": template.name,
            "content": template.content,
            "alignment": template.alignment,
        })

class AgreementSettingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления настройками соглашений.
    """
    queryset = AgreementSettings.objects.all()
    serializer_class = AgreementSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ограничение доступа только к единственной записи (т.к. предполагается одна настройка)
        """
        return super().get_queryset()[:1]

    def update_selected_template(self, request):
        """
        Функция обновления выбранного шаблона
        """
        template_id = request.data.get('template_id')
        if not template_id:
            return Response({
                "error": "Не указан ID шаблона"
            }, status=status.HTTP_400_BAD_REQUEST)

        template = get_object_or_404(PDFTemplate, pk=template_id)
        settings = self.get_queryset().first()
        if not settings:
            settings = AgreementSettings.objects.create(selected_template=template)
        else:
            settings.selected_template = template
            settings.save()

        return Response({
            "message": "Шаблон успешно обновлен",
            "selected_template": PDFTemplateSerializer(template).data,
        })