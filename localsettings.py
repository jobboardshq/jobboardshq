import os
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'zobpress'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = 'niharbala'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = '/home/shabda/jobboard/site_media/'
MEDIA_ROOT = os.path.join(SITE_ROOT, 'site_media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

ROOT_URLCONF = 'urls'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e6v12%-+5u#zr1fz=)2jnn@+9&_7ay8%%&7@sjnf_bxb%z26m-'

EMAIL_SENDER = 'admin@zobpress.com'


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates')
)

WEBFACTION_DEBUG = False

#Email options:
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'emtaccount@gmail.com'
EMAIL_HOST_PASSWORD = 'emtaccountp'
EMAIL_USE_TLS = True



BASE_DOMAIN = 'cc.ll'###VERY VERY IMPORTANT

