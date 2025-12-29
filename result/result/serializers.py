from rest_framework import serializers
from .models import Result
from users.models import User
from main.models import Olympiad
from school.models import School


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения данных ученика.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'school', 'classroom']

    def get_full_name(self, obj):
        return f"{obj.last_name} {obj.first_name} {obj.surname or ''}".strip()


class OlympiadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения данных олимпиады.
    """

    class Meta:
        model = Olympiad
        fields = ['id', 'name', 'stage', 'level', 'class_olympiad', 'category']


class ResultSerializer(serializers.ModelSerializer):
    """
    Основной сериализатор для результатов олимпиад.
    """
    info_children = UserSerializer(read_only=True)  # Вложенный сериализатор для ученика
    info_olympiad = OlympiadSerializer(read_only=True)  # Вложенный сериализатор для олимпиады
    school_name = serializers.CharField(source='school.name', read_only=True)
    status_display = serializers.CharField(source='get_status_result_display', read_only=True)

    class Meta:
        model = Result
        fields = [
            'id', 'info_children', 'info_olympiad', 'points', 'status_result',
            'status_display', 'advanced', 'date_added', 'school', 'school_name'
        ]
        read_only_fields = ['date_added', 'status_display', 'school_name']


class CreateResultSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового результата.
    """

    class Meta:
        model = Result
        fields = [
            'info_children', 'info_olympiad', 'points', 'status_result', 'advanced'
        ]

    def validate(self, data):
        """
        Дополнительная валидация данных.
        """
        user = data.get('info_children')
        olympiad = data.get('info_olympiad')

        if not user or not olympiad:
            raise serializers.ValidationError("Укажите корректного ученика и олимпиаду.")

        if user.school != self.context['request'].user.school:
            raise serializers.ValidationError("Ученики могут быть только из вашей школы.")

        return data


class ImportResultSerializer(serializers.Serializer):
    """
    Сериализатор для импорта результатов из Excel.
    """
    excel_file = serializers.FileField()

    def validate_excel_file(self, value):
        """
        Проверка, что файл имеет корректное расширение.
        """
        if not value.name.endswith(('.xls', '.xlsx')):
            raise serializers.ValidationError("Допустимы только файлы Excel (.xls, .xlsx).")
        return value
