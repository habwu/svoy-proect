from django.urls import path, include
from rest_framework.routers import DefaultRouter
from classroom.views import ClassroomViewSet, UserViewSet

app_name = 'classroom'

router = DefaultRouter()
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),  # Подключение стандартных маршрутов
]
