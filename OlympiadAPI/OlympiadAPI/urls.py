from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from main.views import *
from django.shortcuts import render

urlpatterns = [
    # Админка
    # path('admin/', admin.site.urls),

    # Главная страница
    # path('', StartPage.as_view(), name='start_page'),
    # path('privacy-policy/', lambda request: render(request, 'privacy-policy/privacy-policy.html'),
    #      name='privacy-policy'),

    # Подключение приложений
    path('main/', include('main.urls', namespace='main')),
    # path('docs/', include('docs.urls', namespace='docs')),
    path('files/', include('files.urls', namespace='files')),
    path('register/', include('register.urls', namespace='register')),
    path('result/', include('result.urls', namespace='result')),
    path('school/', include('school.urls', namespace='school')),
    path('manager/', include('manager.urls', namespace='manager')),
    path('classroom/', include('classroom.urls', namespace='classroom')),
    path('calendar/', include('calendar_olimp.urls', namespace='calendar')),
    path('users/', include('users.urls', namespace='users')),
]

# Обработка медиафайлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

