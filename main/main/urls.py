from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OlympiadViewSet

app_name = 'main'

# Создаем роутер для ViewSet
router = DefaultRouter()
router.register(r'olympiads', OlympiadViewSet, basename='olympiad')

urlpatterns = [
    path('', include(router.urls)),  # Автоматическое подключение маршрутов ViewSet
]
