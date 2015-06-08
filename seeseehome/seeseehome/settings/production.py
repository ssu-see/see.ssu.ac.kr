from seeseehome.settings.settings import *


# Set DSN value 
# Why environ.get ? 
# Because Public Travis cannot accept hashed environment variable
# So for pass travis, cannot set that variable
RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
}

# Add raven to the list of installed apps
INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)
