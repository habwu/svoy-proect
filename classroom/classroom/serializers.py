from rest_framework import serializers
from .models import Classroom
from users.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:

        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'surname', 'birth_date',
            'gender', 'classroom', 'is_expelled', 'password', 'classroom_guide', 'subject', 'post_job_teacher',
            'is_expelled'
        ]
        read_only_fields = ['id', 'school']

    def create(self, validated_data):
        PasswordSerial = validated_data.pop('password', None)
        user = User(**validated_data)
        if PasswordSerial:
            user.set_password(PasswordSerial)
        user.save()
        return user

    def update(self, instance, validated_data):
        PasswordUpdate = validated_data.pop('password', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if PasswordUpdate:
            instance.set_password(PasswordUpdate)
        instance.save()
        return instance


class ClassroomSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    child = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'school', 'number', 'letter', 'is_graduated', 'teacher', 'children']
        read_only = ['id', 'school']


class PromoteAllClassroomsSerializer(serializers.Serializer):
    confirm = serializers.BooleanField()


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_new_password(self, value):
        digits = '1234567890'
        upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lower_letters = 'abcdefghijklmnopqrstuvwxyz'
        symbols = '!@#$%^&*()-+'
        acceptable = digits + upper_letters + lower_letters + symbols

        passwd = set(value)
        if any(char not in acceptable for char in passwd):
            print('Ошибка. Запрещенный спецсимвол')
        else:
            recommendations = []
            if len(value) < 12:
                recommendations.append(f'увеличить число символов - {12 - len(value)}')
            for what, message in ((digits, 'цифру'),
                                  (symbols, 'спецсимвол'),
                                  (upper_letters, 'заглавную букву'),
                                  (lower_letters, 'строчную букву')):
                if all(char not in what for char in passwd):
                    recommendations.append(f'добавить 1 {message}')

            if recommendations:
                print("Слабый пароль. Рекомендации:", ", ".join(recommendations))
            else:
                print('Сильный пароль.')
        return value


class StudentPasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_new_password(self, value):
        # Создаем временный экземпляр ChangePasswordSerializer для проверки
        temp_serializer = ChangePasswordSerializer(data={'new_password': value})
        temp_serializer.is_valid(raise_exception=True)  # Проверяем пароль на валидность
        return value


class ExpelStudentSerializer(serializers.Serializer):
    is_expelled = serializers.BooleanField()
