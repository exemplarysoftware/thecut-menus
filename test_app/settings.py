import os
from django import VERSION

# Make filepaths relative to settings. Needed?
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}
USE_TZ = False
SITE_ID = 1
SECRET_KEY = 'thecut-menus'

ROOT_URLCONF = 'test_app.urls'
STATIC_URL = '/static/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_nose',
    'thecut.menus', # TODO: get the `run.sh shell` command running.
]

if VERSION < (1,7,0):
    INSTALLED_APPS.append('south')


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ('--nocapture', )
SOUTH_TESTS_MIGRATE = False
