from django.contrib import admin
from manager.models import SchoolApplication


@admin.register(SchoolApplication)
class SchoolApplicationAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели SchoolApplication в админке.
    """
    list_display = (
        'id',
        'name',
        'applicant_name',
        'contact_email',
        'contact_phone',
        'status',
        'school_created',
        'credentials_sent',
        'created_at',
    )
    search_fields = (
        'name',
        'applicant_name',
        'contact_email',
        'contact_phone',
    )
    list_filter = (
        'status',
        'school_created',
        'credentials_sent',
        'created_at',
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def has_delete_permission(self, request, obj=None):
        """
        Ограничение на удаление объектов в админке.
        """
        return False  # Удаление запрещено в админке
