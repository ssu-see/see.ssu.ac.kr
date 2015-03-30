# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

import os
from seeseehome.settings.partials.application import BASE_DIR


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
