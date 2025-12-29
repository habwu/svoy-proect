from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Модель пользователей в панели администратора."""
    list_display = [
        'id',  # ID пользователя
        'username',  # Имя пользователя
        'first_name',  # Имя
        'last_name',  # Фамилия
        'surname',  # Отчество
        'email',  # Электронная почта
        'gender',  # Пол
        'school',  # Школа
        'is_staff',  # Флаг сотрудника
        'is_active',  # Флаг активности
        'is_admin',  # Флаг администратора
        'is_manager',  # Флаг менеджера
        'is_teacher',  # Флаг учителя
        'is_child',  # Флаг ученика
    ]
    list_editable = [
        'username',  # Имя пользователя
        'first_name',  # Имя
        'last_name',  # Фамилия
        'surname',  # Отчество
        'email',  # Электронная почта
        'is_staff',  # Флаг сотрудника
        'is_active',  # Флаг активности
        'is_admin',  # Флаг администратора
        'is_manager',  # Флаг менеджера
        'is_teacher',  # Флаг учителя
        'is_child',  # Флаг ученика
    ]
    ordering = ['id']  # Сортировка по ID
    search_fields = ['last_name', 'first_name', 'username', 'email']  # Поиск по имени, фамилии, логину и email
    list_filter = ['is_staff', 'is_active', 'is_admin', 'is_manager', 'is_teacher', 'is_child', 'school']  # Фильтры
    fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'password', 'first_name', 'last_name', 'surname', 'email', 'gender', 'birth_date')
        }),
        ('Роли и доступ', {
            'fields': ('is_staff', 'is_active', 'is_admin', 'is_manager', 'is_teacher', 'is_child', 'is_expelled')
        }),
        ('Связи', {
            'fields': ('school', 'classroom', 'classroom_guide', 'subject', 'post_job_teacher')
        }),
        ('Дополнительно', {
            'fields': ('image', 'telegram_id', 'telegram_link_code', 'telegram_link_code_created_at')
        }),
    )
