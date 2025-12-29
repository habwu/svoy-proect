# your_app/admin.py

from django.contrib import admin
from classroom.models import Classroom
from users.models import User

class UserInline(admin.TabularInline):
    """
    Встроенная форма для отображения и редактирования учеников внутри класса.
    """
    model = Classroom.child.through  # Через промежуточную модель ManyToManyField
    extra = 1
    verbose_name = "Ученик"
    verbose_name_plural = "Ученики"
    # Можно ограничить поля, например:
    # fields = ['user']

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели Classroom.
    """
    list_display = [
        'id',
        'number',
        'letter',
        'teacher',
        'is_graduated',
        'graduation_year',
        'active_students_count',
    ]
    list_editable = ['number', 'letter']
    search_fields = [
        'number',
        'letter',
        'teacher__username',
        'teacher__first_name',
        'teacher__last_name',
    ]
    list_filter = ['is_graduated', 'school']
    ordering = ['number', 'letter']
    inlines = [UserInline]
    filter_horizontal = ['child']

    def active_students_count(self, obj):
        """
        Метод для отображения количества активных (не исключенных) учеников в классе.
        """
        return obj.active_students_count()
    active_students_count.short_description = 'Активные ученики'

    def get_queryset(self, request):
        """
        Оптимизация запроса для предзагрузки связанных данных.
        """
        qs = super().get_queryset(request)
        return qs.select_related('teacher', 'school').prefetch_related('child')

    # Дополнительные действия в админке (например, продвижение классов)
    actions = ['promote_selected_classrooms']

    def promote_selected_classrooms(self, request, queryset):
        """
        Кастомное действие для продвижения выбранных классов на следующий уровень или отметки как выпустившиеся.
        """
        for classroom in queryset:
            classroom.promote()
        self.message_user(request, f"Выбранные классы успешно продвинуты.")
    promote_selected_classrooms.short_description = "Продвинуть выбранные классы на следующий уровень"
