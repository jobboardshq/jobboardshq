from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('management.views',
    url(r'^$', 'index', name='manage_index'),
    
)

    