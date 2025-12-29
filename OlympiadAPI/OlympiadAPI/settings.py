import os
from pathlib import Path
from datetime import timedelta
import sys
import pymysql
from celery.schedules import crontab
from decouple import config
from django.contrib.messages import constants as message_constants

pymysql.install_as_MySQLdb()

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, '..'))

# Основные настройки безопасности и режима отладки
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
# Основной файл маршрутов
ROOT_URLCONF = 'OlympiadAPI.urls'

# Интернационализация
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Asia/Yekaterinburg'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Формат ввода дат
DATE_INPUT_FORMATS = '%d-%m-%Y'

# Настройка пользовательской модели пользователя
AUTH_USER_MODEL = 'users.User'

# Настройки сессий
SESSION_COOKIE_AGE = 1209600  # 2 недели
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# URL для перенаправления при входе в систему
LOGIN_URL = 'users:login'

# Доверенные источники CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://api.olimpteam.ru",
    "https://www.api.olimpteam.ru",
]

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Убедитесь, что указана правильная директория
        'APP_DIRS': True,  # Это необходимо для автоматической загрузки шаблонов приложений
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'channels',
    'corsheaders',
    'storages',
    'easy_thumbnails',
    # Мои приложения
    'OlympiadAPI',
    'main',
    'users',
    'docs',
    'register',
    'classroom',
    'result',
    'calendar_olimp',
    'files',
    'school',
    'raiting_system',
    'manager',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# REST Framework настройки
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Настройки JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'SIGNING_KEY': SECRET_KEY,
}

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {'timeout': 20},
    }
}

# Настройки статики и медиа с использованием S3
# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
# AWS_S3_ENDPOINT_URL = f'https://{AWS_S3_REGION_NAME}.timeweb.cloud'
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.timeweb.cloud'
# AWS_QUERYSTRING_AUTH = False
#
# STATICFILES_STORAGE = 'olympiad.storage_backends.StaticStorage'
# DEFAULT_FILE_STORAGE = 'olympiad.storage_backends.MediaStorage'
#
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
#
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'error.log'),
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Настройки Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_BEAT_SCHEDULE = {
    'import_cpkimr_results': {
        'task': 'docs.tasks.import_cpkimr_results_task',
        'schedule': crontab(hour=1, minute=0),
    },
}
