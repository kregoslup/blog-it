import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'nnu5*gfplph1%t1_ocg_8wn2cb#%ygtmi8fva4-5do%p3onh5u'

DEBUG = True

ALLOWED_HOSTS = []

CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
BROKER_URL = "amqp://guest:guest@localhost:5672"
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'

AUTH_USER_MODEL = 'project.apps.blog.User'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'project.apps.blog',
    'project.apps.posts',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.auth',
    'djcelery',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

DJOSER = {
    'DOMAIN': 'frontend.com',
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_CONFIRMATION_EMAIL': True,
}

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'BlogitDB',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'localhost',
        'PORT': '5432',
    }
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
