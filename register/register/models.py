from django.db import models
from users.models import User
from main.models import Olympiad
from school.models import School


class Register(models.Model):
    """
    Модель заявки учеников на олимпиады.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Школа', related_name='registers')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Учитель', blank=True, null=True)
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registers', verbose_name='Ученик')
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, verbose_name='Олимпиада')
    status_send = models.BooleanField(default=False, verbose_name='Статус отправки')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалено')

    class Meta:
        verbose_name = 'Заявка регистрации на олимпиаду'
        verbose_name_plural = 'Заявки регистрации на олимпиады'

    def __str__(self):
        return f"ID {self.id}: {self.child.get_full_name()} - Олимпиада: {self.olympiad.name} (Статус отправки: {self.status_send})"


class RegisterSend(models.Model):
    """
    Модель отправки заявки ученика на олимпиаду учителем.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Школа', related_name='register_sends', blank=True, null=True)
    teacher_send = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Учитель отправитель', blank=True, null=True)
    child_send = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_registers', verbose_name='Ученик')
    olympiad_send = models.ForeignKey(Olympiad, on_delete=models.CASCADE, related_name='sent_registers', verbose_name='Олимпиада')
    status_teacher = models.BooleanField(default=False, verbose_name='Статус учителя')
    status_admin = models.BooleanField(default=False, verbose_name='Статус администратора')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалено')
    status_send = models.BooleanField(default=False, verbose_name='Статус отправки')

    class Meta:
        verbose_name = 'Отправленная заявка'
        verbose_name_plural = 'Отправленные заявки'
        unique_together = ('teacher_send', 'child_send', 'olympiad_send')

    def __str__(self):
        return f"Заявка: Ученик {self.child_send.get_full_name()} - Олимпиада: {self.olympiad_send.name} (Статус учителя: {self.status_teacher})"


class RegisterAdmin(models.Model):
    """
    Модель утверждения заявки администраторами.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Школа', related_name='register_admins')
    teacher_admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель администратор')
    child_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_approved_registers', verbose_name='Ученик')
    olympiad_admin = models.ForeignKey(Olympiad, on_delete=models.CASCADE, related_name='admin_approved_registers', verbose_name='Олимпиада')
    status_admin = models.BooleanField(default=False, verbose_name='Статус администратора')
    status_teacher = models.BooleanField(default=False, verbose_name='Статус учителя')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалено')

    class Meta:
        verbose_name = 'Утверждённая заявка'
        verbose_name_plural = 'Утверждённые заявки'

    def __str__(self):
        return f"Утверждённая заявка: {self.child_admin.get_full_name()} - Олимпиада: {self.olympiad_admin.name} (Статус администратора: {self.status_admin})"


class Recommendation(models.Model):
    """
    Модель рекомендаций для участия в олимпиадах.
    """
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'

    STATUS_CHOICES = [
        (PENDING, 'В ожидании'),
        (ACCEPTED, 'Принято'),
        (DECLINED, 'Отказано учеником'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='recommendations', verbose_name='Школа')
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_recommendations', verbose_name='Рекомендатель')
    recommended_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_recommendations', verbose_name='Кому рекомендовано')
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations', verbose_name='Ученик')
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, verbose_name='Олимпиада')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING, verbose_name='Статус')

    class Meta:
        verbose_name = 'Рекомендация'
        verbose_name_plural = 'Рекомендации'
        unique_together = ('recommended_by', 'recommended_to', 'child', 'olympiad')

    def __str__(self):
        return f"Рекомендация: {self.recommended_by.get_full_name()} -> {self.recommended_to.get_full_name()} для {self.child.get_full_name()} (Олимпиада: {self.olympiad.name})"

    def update_status_if_registered(self):
        """
        Обновление статуса рекомендации на 'Принято', если ученик зарегистрирован на олимпиаду.
        """
        if Register.objects.filter(child=self.child, olympiad=self.olympiad).exists():
            self.status = self.ACCEPTED
            self.save()
