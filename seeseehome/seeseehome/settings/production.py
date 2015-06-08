from .settings import *


# Set DSN value 
# Why environ.get ? 
# Because Public Travis cannot accept hashed environment variable
# So for pass travis, cannot set that variable
RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
}

INSTALLED_APPS += (
    # Add raven to the list of installed appsI
    'raven.contrib.django.raven_compat',

    # Django 3rd Party Modules ( installed via pip )
    'django_nose',
    'django_extensions',
    'debug_toolbar',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Do not set True in Production state
DEBUG = False
TEMPLATE_DEBUG = False
