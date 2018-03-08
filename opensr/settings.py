import os
import environ
import django.conf.global_settings as DEFAULT_SETTINGS
from email.utils import getaddresses

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

env = environ.Env(
    SECRET_KEY=str,
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['127.0.0.1:8000']),
    DATABASE_URL=str,
    ADMINS=str,
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = env('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'django.contrib.messages',
    'bootstrap_admin',
    'django.contrib.admin',
    'test',
    'colorful',
    'ckeditor',
    'sortedm2m'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#   'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
#   'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'opensr.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates')
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

#WSGI_APPLICATION = 'opensr.wsgi.application'


# Authentication

ADMINS = getaddresses([env('ADMINS')])

MANAGERS = ADMINS


# Database

DATABASES = {
    'default': env.db(),
}


# Internationalization

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True
 
USE_TZ = True


# Site definition

SITE_ID = 1

SITE_URL = 'sp'

SITE_NAME = 'OpenSR'


# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'opensr/media')

MEDIA_URL = '/media/'


# Static files

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
#   'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# CKEditor

CKEDITOR_UPLOAD_PATH = os.path.join(PROJECT_DIR, 'media/images')

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'resize_minHeight': 300,
        'width': 600,
        'resize_enabled': False,
    },
}


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
