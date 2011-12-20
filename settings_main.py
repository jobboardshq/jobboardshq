# Django settings for job_board project.\
import os

from settings import *

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    )

INSTALLED_APPS = (
    #'zobpress',
    'sitewide',
    #'emailsubs',
    #'widgets',
    #'management',
    'registration',
    #'profiles',
    #"frontend",
    "compressor",
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'south',
    #'haystack',
    #"pagination",
    'tinymce'
)

LOGIN_REDIRECT_URL = "/redirect-to-board/" 

from localsettings_main import *
