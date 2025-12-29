from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeagueViewSet, MedalViewSet, RatingViewSet, PersonalMedalViewSet

app_name = 'raiting_system'

# Создаем роутер для ViewSet
router = DefaultRouter()
router.register(r'leagues', LeagueViewSet, basename='league')
router.register(r'medals', MedalViewSet, basename='medal')
router.register(r'ratings', RatingViewSet, basename='rating')
router.register(r'personal-medals', PersonalMedalViewSet, basename='personal_medal')

urlpatterns = [
    path('', include(router.urls)),  # Все маршруты для ViewSet
]
