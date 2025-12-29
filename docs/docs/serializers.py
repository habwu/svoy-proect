# serializers.py

from rest_framework import serializers
from classroom.models import Classroom
from files.models import PDFTemplate, AgreementSettings
from main.models import Subject, Olympiad, Category, LevelOlympiad, Stage, Post
from register.models import RegisterAdmin, RegisterSend
from result.models import Result
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LevelOlympiadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelOlympiad
        fields = '__all__'


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class OlympiadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    level = LevelOlympiadSerializer(read_only=True)
    stage = StageSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Olympiad
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # Предполагается, что User имеет поля school, subject (M2M), classroom, classroom_guide и т.д.
    # Если нужно, можно добавить вложенные сериализаторы.
    # Здесь просто пример:
    subject = SubjectSerializer(many=True, read_only=True)
    post_job_teacher = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class ClassroomSerializer(serializers.ModelSerializer):
    # Предполагается, что Classroom имеет поля teacher (User), child (M2M User), school, number, letter
    # В зависимости от модели можно настроить вложенные сериализаторы.
    # Здесь для примера teacher и child отображаются через UserSerializer (read_only).
    teacher = UserSerializer(read_only=True)
    child = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = '__all__'


class PDFTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFTemplate
        fields = '__all__'


class AgreementSettingsSerializer(serializers.ModelSerializer):
    selected_template = PDFTemplateSerializer(read_only=True)

    class Meta:
        model = AgreementSettings
        fields = '__all__'


class RegisterAdminSerializer(serializers.ModelSerializer):
    child_admin = UserSerializer(read_only=True)
    olympiad_admin = OlympiadSerializer(read_only=True)

    class Meta:
        model = RegisterAdmin
        fields = '__all__'


class RegisterSendSerializer(serializers.ModelSerializer):
    child_send = UserSerializer(read_only=True)
    olympiad_send = OlympiadSerializer(read_only=True)

    class Meta:
        model = RegisterSend
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    info_children = UserSerializer(read_only=True)
    info_olympiad = OlympiadSerializer(read_only=True)

    class Meta:
        model = Result
        fields = '__all__'
