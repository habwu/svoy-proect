from django.contrib import admin
from main.models import Subject, Category, LevelOlympiad, Stage, Post, Olympiad, AuditLog


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Управление учебными предметами в админке"""
    list_display = ('id', 'name')
    list_editable = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Управление категориями олимпиад в админке"""
    list_display = ('id', 'name')
    list_editable = ('name',)
    search_fields = ('name',)


@admin.register(LevelOlympiad)
class LevelOlympiadAdmin(admin.ModelAdmin):
    """Управление уровнями олимпиад в админке"""
    list_display = ('id', 'name')
    list_editable = ('name',)
    search_fields = ('name',)


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    """Управление этапами олимпиад в админке"""
    list_display = ('id', 'name')
    list_editable = ('name',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Управление должностями персонала школы в админке"""
    list_display = ('id', 'name')
    list_editable = ('name',)
    search_fields = ('name',)


@admin.register(Olympiad)
class OlympiadAdmin(admin.ModelAdmin):
    """Управление олимпиадами в админке"""
    list_display = (
        'id', 'name', 'description', 'category', 'level', 'stage', 'subject', 'class_olympiad', 'date', 'time',
        'location'
    )
    list_editable = (
    'name', 'description', 'category', 'level', 'stage', 'subject', 'class_olympiad', 'date', 'time', 'location')
    search_fields = ('name', 'class_olympiad', 'category__name', 'level__name', 'stage__name', 'subject__name')
    list_filter = ('category', 'level', 'stage', 'subject', 'date')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Управление журналом аудита в админке"""
    list_display = ('id', 'user', 'action', 'object_name', 'timestamp', 'school')
    search_fields = ('user__username', 'action', 'object_name', 'school__name')
    list_filter = ('timestamp', 'school', 'action')
