from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('widgets.views',
    url(r'^$', 'index', name='widgets_index'),
    url(r'^jobs.js$', 'jobs_js', name='widgets_jobs_js'),
    url(r'^jobs/$', 'jobs_iframe', name='widgets_jobs'),
    url(r'^test/$', 'test_widgets', name='widgets_test'),
)

    