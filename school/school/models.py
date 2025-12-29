from django.db import models


class School(models.Model):
    """
    Модель, представляющая школу с основными контактными данными.
    """
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    SCHOOL_TYPE_CHOICES = [
        ('public', 'Государственная'),
        ('private', 'Частная'),
        ('charter', 'Чартерная'),
    ]

    # Администратор и статус
    admin_user = models.OneToOneField(
        'users.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='admin_user'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус заявки'
    )
    credentials_sent = models.BooleanField(default=False, verbose_name='Данные для входа отправлены')

    # Основная информация
    name_cpkimr = models.CharField(
        max_length=255, unique=True, verbose_name='Название школы в базе CPKIMR', null=True, blank=True
    )
    name = models.CharField(
        max_length=255, unique=True, verbose_name='Название школы', blank=True, null=True
    )
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name='Страна', blank=True, null=True)
    region = models.CharField(max_length=100, verbose_name='Субъект РФ', blank=True, null=True)
    locality = models.CharField(max_length=100, verbose_name='Населенный пункт', blank=True, null=True)
    principal_name = models.CharField(max_length=255, verbose_name='Директор', blank=True, null=True)

    # Контактные данные
    contact_email = models.EmailField(verbose_name='Контактный email', blank=True, null=True)
    contact_phone = models.CharField(max_length=20, verbose_name='Контактный телефон', blank=True, null=True)
    domain = models.CharField(max_length=255, verbose_name='Домен', blank=True, null=True)
    website = models.URLField(blank=True, null=True, verbose_name='Веб-сайт')

    # Дополнительная информация
    established_year = models.PositiveIntegerField(blank=True, null=True, verbose_name='Год основания')
    number_of_students = models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество учащихся')
    school_type = models.CharField(
        max_length=50, blank=True, null=True, choices=SCHOOL_TYPE_CHOICES, verbose_name='Тип школы'
    )
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True, verbose_name='Логотип')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Информация о заявителе
    applicant_name = models.CharField(
        max_length=255, verbose_name='ФИО заполнителя заявки', blank=True, null=True
    )
    applicant_phone = models.CharField(
        max_length=20, verbose_name='Телефон заполнителя заявки', blank=True, null=True
    )
    applicant_email = models.EmailField(verbose_name='E-mail заполнителя заявки', blank=True, null=True)
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        """Возвращает название школы или строку по умолчанию."""
        return self.name or "Без названия"

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'
        ordering = ['name']
