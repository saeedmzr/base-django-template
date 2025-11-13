"""
Django settings for {{cookiecutter.project_slug}} project.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path

from ..env import env

# region GENERAL ---------------------------------------------------------------

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG_MODE')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

APP_DOMAIN = env('APP_DOMAIN', default='http://localhost:8000')

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# endregion --------------------------------------------------------------------

# region URLS ------------------------------------------------------------------

ROOT_URLCONF = '{{cookiecutter.project_slug}}.urls'
WSGI_APPLICATION = '{{cookiecutter.project_slug}}.wsgi.application'

# endregion --------------------------------------------------------------------

# region APPS DEFINITION -------------------------------------------------------

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
{%- if cookiecutter.use_celery == 'y' %}
    'django_celery_results',
    'django_celery_beat',
{%- endif %}
{%- if cookiecutter.use_jwt == 'y' %}
    'rest_framework_simplejwt',
{%- endif %}
{%- if cookiecutter.use_auditlog == 'y' %}
    'auditlog',
{%- endif %}
]

LOCAL_APPS = [
    'apps.users',
    # custom apps go here
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# endregion --------------------------------------------------------------------

# region MIDDLEWARE ------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'auditlog.middleware.AuditlogMiddleware'

]

# endregion --------------------------------------------------------------------

# region DATABASES -------------------------------------------------------------

# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_NAME', default='postgres'),
        'HOST': env('POSTGRES_DB_HOST', default='localhost'),
        'PORT': env('POSTGRES_DB_PORT', default=5432),
        'USER': env('POSTGRES_USER', default='postgres'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='postgres'),
    }
}

# endregion --------------------------------------------------------------------

# region TEMPLATES -------------------------------------------------------------

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

# endregion --------------------------------------------------------------------

# region AUTHENTICATION --------------------------------------------------------

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'users.User'

# endregion --------------------------------------------------------------------

# region PASSWORDS -------------------------------------------------------------

# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]

# endregion --------------------------------------------------------------------

# region REST FRAMEWORK --------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        {%- if cookiecutter.use_jwt == 'n' %}
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        {%- else %}
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        {%- endif %}
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Swagger

SPECTACULAR_SETTINGS = {
    'TITLE': '{{cookiecutter.project_name}} API',
    'DESCRIPTION': 'Documentation of API endpoints of {{cookiecutter.project_name}}',
    'VERSION': '{{cookiecutter.version}}',
}

# endregion --------------------------------------------------------------------

# region CORS ------------------------------------------------------------------

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

# endregion --------------------------------------------------------------------

# region CACHES ----------------------------------------------------------------

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_LOCATION', default='redis://localhost:6379'),
    }
}

CACHE_TTL = 60 * 15  # Cache time to live is 15 minutes.

# endregion --------------------------------------------------------------------
{%- if cookiecutter.use_jwt == 'y' %}

# region JWT -------------------------------------------------------------------

from datetime import timedelta  # noqa

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ['rest_framework_simplejwt.tokens.AccessToken', ],
}

# endregion --------------------------------------------------------------------
{%- endif %}
{%- if cookiecutter.use_celery == 'y' %}

# region CELERY ----------------------------------------------------------------

CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# endregion --------------------------------------------------------------------
{%- endif %}
