from django.urls import path, include
from rest_framework.routers import DefaultRouter

from school.views import *

app_name = 'school'

router = DefaultRouter()
router.register('school', SchoolViewSet, basename='school')
router.register('application', SchoolApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]

