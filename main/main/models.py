from django.db import models


class AuditLog(models.Model):
    """
    Модель для ведения журнала аудита действий пользователей.
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    action = models.CharField(max_length=256, verbose_name='Действие')
    object_name = models.CharField(max_length=256, verbose_name='Объект')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время действия')
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, verbose_name='Школа',
                               related_name='school_audit')

    def __str__(self):
        return f'{self.user} - {self.action} - {self.object_name}'

    class Meta:
        verbose_name_plural = "Журнал аудита"
        verbose_name = "Запись аудита"


class Subject(models.Model):
    """
    Модель учебных предметов.
    """
    name = models.CharField('Название предмета', max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Предметы"
        verbose_name = "Предмет"


class Category(models.Model):
    """
    Модель категорий олимпиад.
    """
    name = models.CharField('Категория', max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории олимпиад"
        verbose_name = "Категория"


class LevelOlympiad(models.Model):
    """
    Модель уровней олимпиад.
    """
    name = models.CharField('Уровень', max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Уровни олимпиад"
        verbose_name = "Уровень"


class Stage(models.Model):
    """
    Модель этапов олимпиад.
    """
    name = models.CharField('Этап', max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Этапы олимпиад"
        verbose_name = "Этап"


class Post(models.Model):
    """
    Модель должностей в школе.
    """
    name = models.CharField('Название должности', max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Должности"
        verbose_name = "Должность"


class Olympiad(models.Model):
    """
    Модель олимпиады.
    """
    name = models.CharField('Название', max_length=256)
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    level = models.ForeignKey(LevelOlympiad, on_delete=models.CASCADE, verbose_name='Уровень')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='Этап')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    class_olympiad = models.PositiveIntegerField('Класс')
    date = models.DateField('Дата проведения', blank=True, null=True)
    time = models.TimeField('Время проведения', blank=True, null=True)
    location = models.CharField('Место проведения', max_length=256, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.stage} - {self.subject} ({self.class_olympiad} класс)'

    class Meta:
        verbose_name_plural = "Олимпиады"
        verbose_name = "Олимпиада"
