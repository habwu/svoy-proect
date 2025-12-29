from rest_framework import serializers
from register.models import Register, RegisterSend, RegisterAdmin, Recommendation
from main.models import Olympiad
from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Register.
    """

    class Meta:
        model = Register
        fields = '__all__'


class RegisterSendSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели RegisterSend.
    """

    class Meta:
        model = RegisterSend
        fields = '__all__'


class RegisterAdminSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели RegisterAdmin.
    """

    class Meta:
        model = RegisterAdmin
        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Recommendation.
    """

    class Meta:
        model = Recommendation
        fields = '__all__'
