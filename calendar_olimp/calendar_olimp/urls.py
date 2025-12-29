from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OlympiadViewSet

app_name = 'calendar_olimp'

router = DefaultRouter()
router.register(r'olympiads', OlympiadViewSet, basename='olympiads')

urlpatterns = [
    path('calendar/', include(router.urls)),
]
