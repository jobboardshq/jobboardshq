from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('sitewide.views',
    url(r'^$', 'index', name='zobpress_index'),
)

    