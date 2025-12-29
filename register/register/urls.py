from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, RegisterSendViewSet, RegisterAdminViewSet, RecommendationViewSet

app_name = 'register'

# Создаем роутер для ViewSet
router = DefaultRouter()
router.register(r'registers', RegisterViewSet, basename='register')
router.register(r'register-sends', RegisterSendViewSet, basename='register-send')
router.register(r'register-admins', RegisterAdminViewSet, basename='register-admin')
router.register(r'recommendations', RecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('', include(router.urls)),  # Все маршруты для ViewSet
]
