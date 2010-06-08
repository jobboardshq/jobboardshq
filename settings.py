# Django settings for job_board project.\
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

FROM_EMAIL = 'messenger@jobboardshq.com'

ADMINS = (
    ("shabda@uswaretech.com", "shabda@uswaretech.com"),
    ("lakshman@uswaretech.com", "lakshman@uswaretech.com"),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'
#TIME_ZONE = 'Asia/Kabul'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'zobpress.middleware.GetSubdomainMiddleware',
    'zobpress.middleware.ThreadLocals',
    'zobpress.middleware.RedirectOnInvalidSubdomain',
    'pagination.middleware.PaginationMiddleware',

)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    'django.contrib.messages.context_processors.messages',
    "zobpress.context_processor.populate_board",
    "frontend.context_processors.board_categories",
    )

HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = (os.path.join(os.path.dirname(__file__), 'search_index/'))




INSTALLED_APPS = (
    'zobpress',
    'sitewide',
    'emailsubs',
    'widgets',
    'management',
    'registration',
    'profiles',
    'frontend',
    'compressor',
    'sorl.thumbnail',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'south',
    'haystack',
    "pagination",
    "mailer",
)

AUTH_PROFILE_MODULE = 'profiles.UserProfile'
ACCOUNT_ACTIVATION_DAYS = 10
UPGRADE_COST = 20
UNALLOWED_SUBDOMAINS = ['www', 'admin', 'zobpress', 'blog']

INDEED_PUBLISHER_ID = '2862623966588653'
INDEED_API_URL = "http://api.indeed.com/ads/apisearch"

BASE_DOMAIN = 'foo.tld'
INTERNAL_IPS = ('127.0.0.1',)

EMAIL_THUMBNAILS = "email"

LOGIN_REDIRECT_URL = "/manage/"

RECAPTCHA_PUBLIC_KEY = '6LcduwsAAAAAANVWknJgRHyqRthPXIZD5bHg-dtn'
RECAPTCHA_PRIVATE_KEY = '6LcduwsAAAAAADgaVqtm6Y5r80v6v8wRWNMfUKyb'

EMAIL_BACKEND = 'mailer.backend.DbBackend'

from localsettings import *

if locals().get('LOCAL_APPS',''):
    INSTALLED_APPS += LOCAL_APPS