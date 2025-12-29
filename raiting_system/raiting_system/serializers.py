from rest_framework import serializers
from .models import League, Medal, Rating, PersonalMedal
from users.models import User
from main.models import Olympiad


class LeagueSerializer(serializers.ModelSerializer):
    """Сериализатор для модели League (Лига)"""

    class Meta:
        model = League
        fields = '__all__'


class MedalSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Medal (Медаль)"""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text="Пользователь, которому принадлежит медаль"
    )
    olympiad = serializers.PrimaryKeyRelatedField(
        queryset=Olympiad.objects.all(),
        help_text="Олимпиада, связанная с медалью"
    )

    class Meta:
        model = Medal
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Rating (Рейтинг)"""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text="Пользователь, для которого указан рейтинг"
    )
    league_display = serializers.CharField(
        source='get_league_display',
        read_only=True,
        help_text="Название лиги в текстовом формате"
    )

    class Meta:
        model = Rating
        fields = ['id', 'user', 'points', 'league', 'league_display']
        read_only_fields = ['league_display']  # Поле только для чтения


class PersonalMedalSerializer(serializers.ModelSerializer):
    """Сериализатор для модели PersonalMedal (Именная медаль)"""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text="Пользователь, которому вручена медаль"
    )

    class Meta:
        model = PersonalMedal
        fields = '__all__'
