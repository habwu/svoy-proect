from django.urls import path, include
from rest_framework.routers import DefaultRouter
from result.views import ResultViewSet

app_name = 'result'

# Создаем роутер для ViewSet
router = DefaultRouter()
router.register(r'', ResultViewSet, basename='result')

urlpatterns = [
    path('', include(router.urls)),  # Все маршруты для ViewSet
]
