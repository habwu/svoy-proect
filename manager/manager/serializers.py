from rest_framework import serializers
from .models import SchoolApplication
from users.models import User
from school.models import School


class SchoolSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели School.
    """

    class Meta:
        model = School
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User, включая связанные данные о школе.
    """
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'school',
        ]


class SchoolApplicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели SchoolApplication, включая связанные данные о школе.
    """
    school = SchoolSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = SchoolApplication
        fields = [
            'id',
            'name',
            'applicant_name',
            'contact_email',
            'contact_phone',
            'status',
            'status_display',
            'school',
            'school_created',
            'credentials_sent',
            'created_at',
        ]
        read_only_fields = ['created_at', 'status_display']
