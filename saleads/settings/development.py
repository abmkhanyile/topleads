from .base_settings import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']