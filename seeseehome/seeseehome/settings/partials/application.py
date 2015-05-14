import os
import warnings


warnings.filterwarnings(
    'ignore', r"DateTimeField .* received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields')

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
BASE_DIR = os.path.abspath(os.path.dirname(__file__) + "../../../../")
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

SECRET_KEY = 't6g+nq2ba%na%(fxbm%ino##c@4+pn&+68j5spm+!nu2e)*6^b'

# Application definition
INSTALLED_APPS = (
    # Custom admin, must set before django.contrib.admin
    'grappelli',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps
    'users',
    'boards',
    'linkboard',

    # Django Packages
    'ckeditor',
    'multiselectfield',
    'nocaptcha_recaptcha',
    'captcha',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # Django Default
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",

    # Custom context processors
    'seeseehome.context_processors.board_list',
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

LOGIN_URL = "/sign-in/"
# If next isn't provided, it redirects to
LOGIN_REDIRECT_URL = "/"

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = \
    '/static/js/jquery-latest.js'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_Full': [
            ["Styles", "Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker", "Undo", "Redo"],
            ["Link", "Unlink", "Anchor"],
            ["attachment", "Image", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
            ["Source"]
        ],
        'language': 'ko-kr',
        'width': '100%',
        'height': '400px',
    },
}

# specify the custom model as the default user model
AUTH_USER_MODEL = 'users.User'

# Grapelli admin settings
GRAPPELLI_ADMIN_TITLE = 'Soongsil Electronic Exhibition'

# Captcha
try:
    RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_SITE_KEY']
    RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_SECRET_KEY']
except:
    RECAPTCHA_PUBLIC_KEY = "need captcha site key"
    RECAPTCHA_PRIVATE_KEY = "need captcha secret key"

NOCAPTCHA = True
RECAPTCHA_USE_SSL = True
