from django.db import models
from users.models import User


class PDFTemplate(models.Model):
    """
    Модель для хранения шаблонов PDF
    """
    ALIGNMENT_CHOICES = [
        ('left', 'Влево'),
        ('center', 'По центру'),
        ('right', 'Вправо'),
    ]
    name = models.CharField(
        max_length=255,
        verbose_name='Название шаблона',
        help_text='Название, отображаемого шаблона'
    )
    content = models.TextField(
        verbose_name='Содержимое шаблона',
        help_text='Используйте HTML для форматирования текста.'
    )
    alignment = models.CharField(
        max_length=10,
        choices=ALIGNMENT_CHOICES,
        default='left',
        verbose_name='Выравнивание текста'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Дата и время создания шаблона.'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
        help_text='Дата и время обновления шаблона.'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Обновлено пользователем',
        help_text='Пользователь, который вносил изменения'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'PDF шаблон'
        verbose_name_plural = 'PDF шаблоны'
        ordering = ['-updated_at']


class AgreementSettings(models.Model):
    """
    Модель для управления настройками соглашений.
    """
    selected_template = models.ForeignKey(
        PDFTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Выбранный шаблон',
        related_name='agreement_settings'
    )
    allow_send_applications = models.BooleanField(
        default=False,
        verbose_name='Разрешить отправку заявок',
        help_text='Указывает, разрешено ли отправлять заявки пользователям.'
    )

    def __str__(self):
        return f'Настройки соглашений - Шаблон: {self.selected_template.name if self.selected_template else "Не выбран"}'

    class Meta:
        verbose_name = 'Настройка соглашений'
        verbose_name_plural = 'Настройки соглашений'
