
from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv
from decouple import config

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

INFOBIP_AUTH_TOKEN = os.environ.get('INFOBIP_AUTH_TOKEN')
INFOBIP_NUMBER = os.environ.get('INFOBIP_NUMBER')
AIT_API_KEY = os.getenv('AIT_API_KEY')
AIT_USERNAME = os.getenv('AIT_USERNAME')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config('DEBUG', cast=bool)
# DEBUG = True
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "corsheaders",
    # 'djoser',
    'social_django',
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    'drf_spectacular',
    'cloudinary_storage',
    'cloudinary',
    'accounts',
    'business',
    'silk',
]

MIDDLEWARE = [
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (BASE_DIR, 'templates'),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = os.environ.get('DATABASE_URL', None)

if not DATABASE_URL:

    DATABASES = {
        # 'default': {
        #     'ENGINE': 'django.db.backends.postgresql',
        #     'NAME': 'autolead_local',
        #     'USER': 'postgres',
        #     'PASSWORD': 'payboi',
        #     'HOST': 'localhost',
        #     'PORT': '5432',
        # },
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },

        'silk': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'silk_db.sqlite3',
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('NAME'),
            'USER': os.environ.get('USER'),
            'PASSWORD': os.environ.get('PASSWORD'),
            'HOST': os.environ.get('HOST'),
            'PORT': os.environ.get('DB_PORT'),
            'OPTIONS': {'sslmode': 'require'}
        },
        'silk': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'silk_db.sqlite3',
        }
    }


if not DEBUG:
    SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# EMAIL BACKEND SETUP

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
# Optional Celery settings
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_SOFT_TIME_LIMIT = 300  # Soft time limit for tasks
CELERY_TASK_TIME_LIMIT = 600  # Hard time limit for tasks


# SENDCHAMP_API_KEY = os.environ.get('SENDCHAMP_API_KEY')

# SENDCHAMP_API_KEY = os.environ.get('SENDCHAMP_API_KEY')
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        "rest_framework.permissions.IsAuthenticated",
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "AutoLeads Project",
    "DESCRIPTION": "PrimeClick AutoLeads Project",
    "VERSION": "1.0.0",
    # OTHER SETTINGS
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://localhost:8000",
)


SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    # 'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=90)
}


SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_MAX_REQUEST_BODY_SIZE = -1  # or another appropriate value
SILKY_MAX_RESPONSE_BODY_SIZE = 1024  # or another appropriate value


# DJOSER = {
#     'LOGIN_FIELD': 'email',
#     'USER_CREATE_PASSWORD_RETYPE': True,
#     'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
#     'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
#     'SEND_CONFIRMATION_EMAIL': True,
#     'SET_PASSWORD_RETYPE': True,
#     'PASSWORD_RESET_CONFIRM_URL': '/password/reset/confirm/{uid}/{token}',
#     'USERNAME_RESET_CONFIRM_URL': '/email/reset/confirm/{uid}/{token}',
#     'ACTIVATION_URL': '/activate/{uid}/{token}',
#     'SEND_ACTIVATION_EMAIL': True,
#     'SERIALIZERS': {
#         'user_create': 'accounts.serializers.UserCreateSerializer',
#         'user': 'accounts.serializers.UserCreateSerializer',
#         'current_user': 'accounts.serializers.UserCreateSerializer',
#         'user_delete': 'djoser.serializers.UserDeleteSerializer'
#     }
# }

GOOGLE_SHEET_API_CREDS = os.path.join(
    BASE_DIR, 'autoleads-402705-e07105ff59b4.json')

MIN_PASSWORD_LENGTH = 8

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['https://www.googleapis.com/auth/userinfo.email',
#                                    'https://www.googleapis.com/auth/userinfo.profile', 'openid']
# SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "djwh3low0",
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

AUTH_USER_MODEL = 'accounts.User'
