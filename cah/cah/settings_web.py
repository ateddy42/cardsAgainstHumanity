from settings import *

DEBUG = False

TEMPLATE_DEBUG = False

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
