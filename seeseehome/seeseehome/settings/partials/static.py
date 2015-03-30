# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

import os
from .application import BASE_DIR


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# This setting defines the additional locations
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)
