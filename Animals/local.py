import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# local environment config file
DEBUG = True
ALLOWED_HOSTS = []
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j#%tnwp%y@#_qb9gz4fkda!o29i%m7on$mhonebu=_=^^8+&1w'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
