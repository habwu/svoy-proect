from rest_framework import serializers
from .models import AuditLog, Olympiad
from users.serializers import UserSerializer


class AuditLogSerializer(serializers.ModelSerializer):
    """
    Сериализатор для журнала аудита.
    """
    user = UserSerializer()

    class Meta:
        model = AuditLog
        fields = '__all__'


class OlympiadSerializer(serializers.ModelSerializer):
    """
    Основной сериализатор для олимпиад.
    """

    class Meta:
        model = Olympiad
        fields = '__all__'


class CreateOlympiadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания олимпиады.
    """

    class Meta:
        model = Olympiad
        fields = '__all__'


class UpdateOlympiadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления олимпиады.
    """

    class Meta:
        model = Olympiad
        fields = ['name', 'description', 'date', 'time', 'location']


class HomePageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления главной страницы.
    """

    class Meta:
        model = UserSerializer.Meta.model
        fields = ['id', 'username', 'email']
