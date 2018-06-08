from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cy%fvop2%6b@-cu#l00ugkxay&jpkd(aegcr-2bc-#78#5!d9+'

DEBUG = env.bool('DJANGO_DEBUG', default=True)
