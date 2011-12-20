import os, sys,site
sys.path.append('/usr/local/lib/python2.7/dist-packages/django/')
sys.path.append('/home/gonecrazy/agiliq_zobpress/')
site.addsitedir("/home/gonecrazy/.virtualenvs/agiliq_zobpress/local/lib/python2.7/site-packages")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()