from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('sitewide.views',
    url(r'^$', 'index', name='sitewide_index'),
    url(r'^register/$', 'register_board', name='sitewide_register_board'),
)

    