"""
Django settings for seeseehome project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# exception message handling
# when we are attempt to save a naive datetime, warning occurs
# During development, such warnings into ignore status
import warnings
warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't6g+nq2ba%na%(fxbm%ino##c@4+pn&+68j5spm+!nu2e)*6^b'

# SECURITY WARNING: don't run with debug turned on in production!
# If you still need to server static locally (e.g. for testing without debug) you can run devserver in insecure mode:
# python manage.py runserver 0.0.0.0:80 --insecure
DEBUG = True
TEMPLATE_DEBUG = False

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '220.149.86.220', 'see.ssu.ac.kr', '0.0.0.0']
#ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#   Custom apps
    'users',
    'boards',
    'linkboard',

#   Django Packages
    'ckeditor',
    'multiselectfield',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

SENDFILE_BACKEND = 'sendfile.backends.development'
# 'sendfile.backends.simple'
# 'sendfile.backends.xsendfile'
# 'sendfile.backends.mod_wsgi'
# 'sendfile.backends.nginx'

ROOT_URLCONF = 'seeseehome.urls'

WSGI_APPLICATION = 'seeseehome.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# This setting defines the additional locations
STATICFILES_DIRS = (
   os.path.join(BASE_DIR, 'static'),
   os.path.join(BASE_DIR, 'assets'),
)

LOGIN_URL = "/sign-in/"
# If next isn't provided, it redirects to
LOGIN_REDIRECT_URL = "/"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
MEDIA_ENABLED = True
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = \
    '/static/js/jquery-latest.js'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_Full' : [
            ["Styles", "Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker", "Undo", "Redo"],
            ["Link", "Unlink", "Anchor"],
            ["attachment", "Image", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
            ["Source"]
            ],
        'language': 'ko-kr',
        'width' : '100%',
        'height': '400px',
    },
}

# specify the custom model as the default user model
AUTH_USER_MODEL = 'users.User'
