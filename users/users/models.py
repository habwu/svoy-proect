from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Расширенная модель пользователя с дополнительными полями.
    """
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = [
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    ]

    image = models.ImageField(
        upload_to='users_images',
        null=True, blank=True,
        verbose_name='Аватар'
    )
    surname = models.CharField(
        "Отчество пользователя (при наличии)", max_length=256, blank=True, null=True
    )
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    gender = models.CharField("Пол", max_length=2, choices=GENDER_CHOICES, blank=True, null=True)
    telegram_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='Telegram ID')
    telegram_link_code = models.CharField(max_length=32, blank=True, null=True, verbose_name='Код привязки Telegram')
    telegram_link_code_created_at = models.DateTimeField(
        blank=True, null=True, verbose_name='Время создания кода привязки'
    )
    is_teacher = models.BooleanField("Учитель", default=False)
    is_child = models.BooleanField("Ученик", default=False)
    is_admin = models.BooleanField("Администратор", default=False)
    is_manager = models.BooleanField("Управляющий сайтом", default=False)
    is_expelled = models.BooleanField("Исключен", default=False)
    classroom_guide = models.ForeignKey(
        'classroom.Classroom', related_name='classroom_teachers', blank=True,
        on_delete=models.SET_NULL, null=True, verbose_name='Классное руководство'
    )
    subject = models.ManyToManyField(
        to="main.Subject", verbose_name="Предметы, которые ведёт учитель",
        blank=True
    )
    post_job_teacher = models.ManyToManyField(
        to="main.Post", verbose_name="Должности учителя",
        blank=True
    )
    classroom = models.ForeignKey(
        'classroom.Classroom', on_delete=models.SET_NULL, verbose_name='Класс ученика',
        blank=True, null=True, related_name='students'
    )
    school = models.ForeignKey(
        'school.School', on_delete=models.CASCADE, related_name='users',
        blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        roles = {
            'is_manager': "Управляющий сайтом",
            'is_teacher': "Учитель",
            'is_admin': "Администратор",
            'is_child': "Ученик"
        }
        for role, role_name in roles.items():
            if getattr(self, role):
                return f"{role_name}: {self.get_full_name()}"
        return f"Пользователь: {self.get_full_name()}"

    def get_full_name(self):
        """Возвращает полное имя пользователя."""
        full_name = f"{self.last_name} {self.first_name} {self.surname or ''}".strip()
        return full_name

    @classmethod
    def get_teachers(cls):
        """Получить всех учителей."""
        return cls.objects.filter(is_teacher=True)

    @classmethod
    def get_children(cls):
        """Получить всех учеников."""
        return cls.objects.filter(is_child=True)

    def get_gender_display(self):
        """Человекочитаемое отображение пола."""
        return dict(self.GENDER_CHOICES).get(self.gender, 'Не указан')

    def get_class_info(self):
        """Информация о классе ученика."""
        if self.classroom:
            return f"{self.classroom.number}{self.classroom.letter}"
        return "Без класса"
