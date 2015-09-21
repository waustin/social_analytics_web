from base import *

DEBUG = False

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en//ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Static asset configuration
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'staticfiles')

# Upload file configuration
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'uploadfiles')
