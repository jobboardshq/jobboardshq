from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('emailsubs.views',
    url(r'^$', 'index', name='emailsubs_index'),
    url(r'^done/$', direct_to_template, {'template':'emailsubs/opted_in.html'}, name='emailsubs_index_done'),
    url(r'^confirm/(?P<id>\d+)/$', 'confirm', name='emailsubs_confirm'),
    url(r'^confirm/done/$', direct_to_template, {'template_name':'emailsubs/email_confirmed.html'}, name='emailsubs_confirm_done'),
    url(r'^unsubscribe/(?P<id>\d+)/$', 'unsubscribe', name='emailsubs_unsubscribe'),
)
