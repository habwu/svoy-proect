from rest_framework import serializers
from main.models import Olympiad


class OlympiadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Olympiad.
    """
    class Meta:
        model = Olympiad
        fields = ['id', 'name', 'date', 'description', 'location']
