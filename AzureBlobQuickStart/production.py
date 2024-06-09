from .settings import *
import os

from .settings import BASE_DIR 
# Configure the domain name using the environment variable
# that Azure automatically creates for us.
#ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
ALLOWED_Hosts = [os.environ['WEBSITE_HOSTNAME']] 
CSRF_TRUSTED_ORIGIN = ['https://' + os.environ['WEBSITE_HOSTNAME']]
DEBUG = False
SECRET_KEY = os.environ['MY_SECRET_KEY']     #make sure that you create this key into Azure Portal 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
CONNECTION = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']

CONNECTION_STR = {pair.split('=')[0]:pair.split('=')[1] for pair in CONNECTION.split('')}
                                                                                     
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": CONNECTION_STR['dbname'],
        "HOST": CONNECTION_STR['host'],
        "USER": CONNECTION_STR['user'],
        "PASSWORD": CONNECTION_STR['password'],
                   }
    }
STATIC_ROOT = BASE_DIR/'staticfiles'

