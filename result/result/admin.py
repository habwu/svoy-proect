from django.contrib import admin
from result.models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """Настройки отображения модели Result в панели администратора."""

    # Поля для отображения в списке
    list_display = ('id', 'info_children', 'info_olympiad', 'points', 'status_result', 'date_added', 'school')

    # Поля, доступные для редактирования в списке
    list_editable = ['points', 'status_result']

    # Поля для поиска
    search_fields = ['info_children__last_name', 'info_children__first_name',
                     'info_children__surname', 'info_olympiad__name']

    # Сортировка по умолчанию
    ordering = ['-date_added', 'id']

    # Фильтры в боковой панели
    list_filter = ['status_result', 'info_olympiad__stage', 'info_olympiad__level', 'school']

    # Поля для отображения детальной информации
    readonly_fields = ['date_added']

    # Настройка оформления
    fieldsets = (
        ('Основная информация', {
            'fields': ('info_children', 'info_olympiad', 'school', 'date_added'),
        }),
        ('Результаты', {
            'fields': ('points', 'status_result', 'advanced'),
        }),
    )

    # Добавление дополнительных действий
    actions = ['mark_as_advanced']

    @admin.action(description='Отметить как прошедшие на следующий этап')
    def mark_as_advanced(self, request, queryset):
        queryset.update(advanced=True)
        self.message_user(request, f'Отмечено {queryset.count()} результатов как "Прошедшие на следующий этап".')
