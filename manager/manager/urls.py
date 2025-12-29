from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolApplicationViewSet

app_name = 'manager'

# Создаем маршруты для ViewSet
router = DefaultRouter()
router.register(r'applications', SchoolApplicationViewSet, basename='school-application')

urlpatterns = [
    path('', include(router.urls)),  # Добавляем маршруты ViewSet
]
