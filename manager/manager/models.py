from django.db import models
from school.models import School


class SchoolApplication(models.Model):
    """
    Модель для хранения заявок на создание школ.
    """
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'В ожидании'),
        (STATUS_APPROVED, 'Подтверждена'),
        (STATUS_REJECTED, 'Отклонена'),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name='Название школы'
    )
    applicant_name = models.CharField(
        max_length=255,
        verbose_name='Имя заявителя'
    )
    contact_email = models.EmailField(
        verbose_name='Контактный email'
    )
    contact_phone = models.CharField(
        max_length=15,
        verbose_name='Контактный телефон'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name='Статус заявки'
    )
    school_created = models.BooleanField(
        default=False,
        verbose_name='Школа создана'
    )
    school = models.OneToOneField(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Школа',
        related_name='application'
    )
    credentials_sent = models.BooleanField(
        default=False,
        verbose_name='Учётные данные отправлены'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подачи заявки'
    )

    def __str__(self):
        """
        Возвращает строковое представление заявки, состоящее из названия школы и имени заявителя.
        """
        return f"{self.name} - {self.applicant_name}"
