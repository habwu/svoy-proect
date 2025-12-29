from rest_framework import serializers
from .models import PDFTemplate, AgreementSettings


class PDFTemplateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели PDFTemplate
    """

    class Meta:
        model = PDFTemplate
        fields = ['id', 'name', 'content', 'alignment', 'created_at', 'updated_at', 'updated_by']
        read_only_fields = ['created_at', 'updated_at', 'updated_by']


class AgreementSettingsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели AgreementSettings
    """
    selected_template = PDFTemplateSerializer(read_only=True)

    class Meta:
        model = AgreementSettings
        fields = ['id', 'selected_template', 'allow_send_applications']
