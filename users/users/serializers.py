from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения информации о пользователях."""
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'surname', 'email',
            'gender', 'birth_date', 'image', 'cropped_image', 'telegram_id',
            'is_teacher', 'is_child', 'is_admin', 'is_manager', 'is_expelled',
            'classroom_guide', 'classroom', 'school', 'subject', 'post_job_teacher', 'full_name'
        ]
        read_only_fields = ['id', 'full_name', 'cropped_image']

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name} {obj.surname}'.strip()


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователей."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'first_name', 'last_name', 'surname', 'email',
            'gender', 'birth_date', 'school', 'classroom', 'is_teacher', 'is_child', 'is_admin', 'is_manager'
        ]

    def create(self, validated_data):
        # Используем метод create_user для хэширования пароля
        return User.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования профиля пользователя."""
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'surname', 'email',
            'gender', 'birth_date', 'image', 'cropped_image', 'telegram_id',
            'classroom', 'school', 'full_name'
        ]
        read_only_fields = ['id', 'full_name', 'cropped_image', 'school']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def update(self, instance, validated_data):
        # Обновляем только разрешенные поля
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
