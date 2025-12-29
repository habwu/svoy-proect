from django.contrib import admin
from .models import Rating, Medal, League, PersonalMedal
from result.models import Result


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Админ-панель для модели рейтинга"""
    list_display = ('id', 'user', 'points', 'league')  # Отображаемые поля в списке
    search_fields = ('user__username', 'user__last_name', 'league')  # Поля для поиска
    list_filter = ('league',)  # Фильтры по лигам
    ordering = ('-points',)  # Сортировка по очкам (убыванию)


@admin.register(Medal)
class MedalAdmin(admin.ModelAdmin):
    """Админ-панель для модели медали"""
    list_display = ('id', 'type', 'user', 'olympiad')  # Отображаемые поля в списке
    search_fields = ('user__username', 'user__last_name', 'olympiad__name')  # Поля для поиска
    list_filter = ('type',)  # Фильтры по типу медали
    ordering = ('-id',)  # Сортировка по ID (убыванию)


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    """Админ-панель для модели лиги"""
    list_display = ('id', 'type', 'min_points', 'max_points')  # Отображаемые поля в списке
    search_fields = ('type',)  # Поля для поиска
    ordering = ('min_points',)  # Сортировка по минимальному количеству очков


@admin.register(PersonalMedal)
class PersonalMedalAdmin(admin.ModelAdmin):
    """Админ-панель для модели именной медали"""
    list_display = ('id', 'name', 'user', 'date_awarded')  # Отображаемые поля в списке
    search_fields = ('name', 'user__username', 'user__last_name')  # Поля для поиска
    list_filter = ('date_awarded',)  # Фильтр по дате вручения
    ordering = ('-date_awarded',)  # Сортировка по дате вручения (убыванию)
