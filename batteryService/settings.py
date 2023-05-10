from decouple import config

from datetime import timedelta

from dj_database_url import parse

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='not avaliable')
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ["*"]

LOCAL_APPS = [
    'usuario',
    'core',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # THIRD-PARTY
    'corsheaders',
    'django_filters',
    'phonenumber_field',
    'rest_framework',
    'rest_framework.authtoken'
] + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'batteryService.urls'

APPEND_SLASH = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'batteryService.wsgi.application'

DATABASE_URL = 'postgres://postgres:postgres@postgres:5432/postgres'
DATABASES = {
    'default': config('DATABASE_URL', default=DATABASE_URL, cast=parse)
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DATE_FORMAT = 'd/m/Y'

PHONENUMBER_DEFAULT_REGION = 'BR'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = config('STATIC_URL', default='/static/')

# Storage
# DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage' if ENV == 'Production' else 'django.core.files.storage.FileSystemStorage'
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
# AZURE_CONNECTION_STRING = config('AZURE_CONNECTION_STRING', '')
# AZURE_CONTAINER = 'images'
MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'usuario.usuario'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Classes defaults utilizadas
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DATE_FORMAT': '%Y-%m-%d',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    # Campo identificador padrão do usuario
    'USER_ID_FIELD': 'id',
}
