from settings import *


# SECRET_KEY = 'e7w-48$!$26l&w-@hgspg*eji)wwl*wu*l_06q@d!jy28xa8d6'

DEBUG = False

TEMPLATES[0]['Debug'] = False

ALLOWED_HOSTS = ['.alphasigcornell.org']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alphasi4_cah',
        'USER': 'alphasi4_cah',
        'PASSWORD': 'KaushikTeddy',
    }
}

STATIC_URL = 'http://cahstatic.alphasigcornell.org/'

STATIC_ROOT = '/home/alphasi4/public_html/cahstatic'
