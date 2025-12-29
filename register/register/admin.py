from django.contrib import admin
from register.models import Register, RegisterSend, RegisterAdmin, Recommendation


class BaseRegisterAdmin(admin.ModelAdmin):
    """Базовый класс для админ-настроек моделей заявок"""
    search_fields = ('school__name',)
    ordering = ('id',)


@admin.register(Register)
class RegisterAdminModel(BaseRegisterAdmin):
    """Настройка админ-панели для модели Register"""
    list_display = ('id', 'school', 'teacher', 'child', 'olympiad', 'status_send', 'is_deleted')
    list_filter = ('status_send', 'is_deleted', 'school')


@admin.register(RegisterSend)
class RegisterSendAdminModel(BaseRegisterAdmin):
    """Настройка админ-панели для модели RegisterSend"""
    list_display = (
        'id', 'school', 'teacher_send', 'child_send', 'olympiad_send',
        'status_teacher', 'status_admin', 'status_send', 'is_deleted'
    )
    list_filter = ('status_teacher', 'status_admin', 'status_send', 'is_deleted')


@admin.register(RegisterAdmin)
class RegisterAdminAdminModel(BaseRegisterAdmin):
    """Настройка админ-панели для модели RegisterAdmin"""
    list_display = (
        'id', 'school', 'teacher_admin', 'child_admin', 'olympiad_admin',
        'status_admin', 'status_teacher', 'is_deleted'
    )
    list_filter = ('status_admin', 'status_teacher', 'is_deleted')


@admin.register(Recommendation)
class RecommendationAdminModel(BaseRegisterAdmin):
    """Настройка админ-панели для модели Recommendation"""
    list_display = ('id', 'school', 'recommended_by', 'recommended_to', 'child', 'olympiad', 'status')
    list_filter = ('status', 'school')
    search_fields = (
        'recommended_by__last_name', 'recommended_by__first_name',
        'recommended_to__last_name', 'recommended_to__first_name',
        'child__last_name', 'child__first_name', 'olympiad__name'
    )
    actions = ['set_to_pending']

    def set_to_pending(self, request, queryset):
        """Перевод выбранных рекомендаций в статус 'В ожидании'"""
        updated = queryset.update(status=Recommendation.PENDING)
        self.message_user(request, f'{updated} рекомендаций переведено в статус "В ожидании".')

    set_to_pending.short_description = 'Перевести в статус "В ожидании"'
