from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'files'

router = DefaultRouter()
router.register(r'pdf-templates', PDFTemplateViewSet, basename='pdf-templates')
router.register(r'settings', AgreementSettingsViewSet, basename='settings')
urlpatterns = [
    path('', include(router.urls)),
]
