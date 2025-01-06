import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_NAME = os.environ.get('PROJECT_NAME', 'my_project')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Application definition
DJANGO_APPS = [
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PART_APPS = [
    'corsheaders',
    'drf_yasg',
    'rest_framework',
]

LOCAL_APPS = [
    'backend.accounts',
    'backend.books',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PART_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Add Corsheaders
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = f'{PROJECT_NAME}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = f'{PROJECT_NAME}.wsgi.application'

# Password validation
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
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Internationalization
LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # Verifica que este directorio exista
]
#STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MongoDB Configuration
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB_NAME = os.environ.get('MONGO_INITDB_DATABASE', 'my_database')
MONGO_DB_USER = os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'user')
MONGO_DB_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'pass')

AUTHENTICATION_BACKENDS = ['backend.accounts.backends.NoAuthBackend']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
    ],
    'UNAUTHENTICATED_USER': None,
    'UNAUTHENTICATED_TOKEN': None,
}

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    #'x-csrftoken',
    'x-requested-with'
]
CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    # http
    'http://localhost:3016',
    # https
    'https://localhost:3016',
] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`

CORS_ORIGIN_REGEX_WHITELIST = [
    # http
    'http://localhost:3016',
    # https
    'https://localhost:3016',
]

redis_host = os.environ.get('REDIS_HOST', 'redis://redis')

CACHES = {
    "default": {
        "BACKEND": 'redis_cache.RedisCache',
        "LOCATION": redis_host,
        "OPTIONS": {
            "DB": 0,
            #"PICKLE_VERSION": 2,
            "SOCKET_CONNECT_TIMEOUT": 1,
            "SOCKET_TIMEOUT": 2,
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "CONNECTION_POOL_CLASS": "redis.ConnectionPool",
        },
    }
}

PREFIX_URL = os.environ.get('PREFIX_URL', '')

if PREFIX_URL != '':
    PREFIX_URL = '%s/' % PREFIX_URL

APPEND_SLASH = True