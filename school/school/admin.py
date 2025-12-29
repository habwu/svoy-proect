from django.contrib import admin
from school.models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    """
    Административная панель для модели School.
    """
    list_display = ('name', 'status', 'address', 'contact_email', 'contact_phone', 'admin_user')  # Поля в списке
    list_filter = ('status', 'school_type', 'region', 'country')  # Фильтры в панели администратора
    search_fields = ('name', 'address', 'contact_email', 'contact_phone', 'admin_user__username')  # Поля для поиска
    readonly_fields = ('created_at', 'updated_at')  # Только для чтения
    ordering = ('name',)  # Сортировка по названию

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'status', 'admin_user', 'description', 'logo')
        }),
        ('Контактные данные', {
            'fields': ('address', 'contact_email', 'contact_phone', 'website', 'domain')
        }),
        ('Дополнительно', {
            'fields': ('country', 'region', 'locality', 'established_year', 'number_of_students', 'school_type')
        }),
        ('Заявка', {
            'fields': ('applicant_name', 'applicant_phone', 'applicant_email', 'comment')
        }),
    )
