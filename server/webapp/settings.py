"""
Django settings for webapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
from commonssite.private import DJANGO_SECRET_KEY
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.insert(0,os.path.join(BASE_DIR, 'weather'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'static/templates/'),
    )

ALLOWED_HOSTS = []

MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'timeseries',
    'hvac',
    'electric',
    'solar',
    'south',
    'weather',
    'arduino',
    'water',
    'learn',
    'projects',
    'markdown_deux', # allows templates to filter text through markdown parser
    'haystack', # 3rd party search engine. used to search for projects.
    'dummy', 
    'colorful' # 3rd party mini-app enabling RGB color-picker field (used in projects.Tag)
    )

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
        },
        # Allow raw HTML
        # (NOTE: not safe for general user input, but OK for admin-generated content!)
        "safe_mode": False
    },
}

HAYSTACK_CONNECTIONS = {
    'default': {
        # whoosh is a 3rd-party text indexer. makes things searchable by haystack.
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH' : os.path.join(BASE_DIR, 'whoosh_index')
    }
}
HAYSTACK_SIGNAL_PROCESSOR = 'projects.signals.IndexUpdateSignalProcessor'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "timeseries.context_processors.systems_schema",
    "timeseries.context_processors.theme",)

ROOT_URLCONF = 'webapp.urls'

WSGI_APPLICATION = 'webapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Load User and Password from my custom location
import commonssite.settings as s

with open(s.sql_credentials, 'r') as f:
    host = f.readline().strip()
    un = f.readline().strip()
    pw = f.readline().strip()
    socket = f.readline().strip()

    DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'HOST' : socket,
    'NAME' : 'commons',
    'USER' : un,
    'PASSWORD' : pw
    }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    )
STATIC_ROOT = os.path.join(BASE_DIR, "static-collected/")
