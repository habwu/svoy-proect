# classroom/models.py

from django.db import models
from datetime import datetime
from users.models import User


class Classroom(models.Model):
    """Модель для представления класса в школе"""

    number = models.IntegerField('Цифра', blank=True, null=True)
    letter = models.CharField('Буква', max_length=1, blank=True, null=True)
    teacher = models.ForeignKey(
        'users.User', blank=True, null=True, on_delete=models.SET_NULL, related_name='teachers', verbose_name='Учитель'
    )
    child = models.ManyToManyField(
        'users.User', blank=True, related_name='childs', verbose_name='Ученики'
    )
    is_graduated = models.BooleanField('Выпустился', default=False)
    graduation_year = models.IntegerField('Год выпуска', blank=True, null=True)
    school = models.ForeignKey(
        'school.School', on_delete=models.CASCADE, verbose_name='Школа', related_name='schools'
    )

    def __str__(self):
        return f'{self.number}{self.letter} - {self.teacher.get_full_name() if self.teacher else "Без учителя"}'

    def promote(self):
        """Метод для продвижения класса на следующий уровень или отметки как выпустившегося"""
        if self.number is not None and self.number < 11:
            self.number += 1
        else:
            self.is_graduated = True
            self.graduation_year = datetime.now().year
        self.save()

    def active_students_count(self):
        """Метод для подсчета числа учеников, которые не исключены"""
        return self.students.filter(is_expelled=False).count()

    @property
    def students(self):
        """Возвращает QuerySet учеников, принадлежащих этому классу"""
        return User.objects.filter(classroom=self, is_child=True)
