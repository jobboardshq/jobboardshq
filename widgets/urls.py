from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('widgets.views',
    url('^jobs.js$', 'jobs_js', name='widgets_jobs_js'),
    url('^jobs/$', 'jobs_iframe', name='widgets_jobs'),
    url('^people.js$', 'people_js', name='widgets_people_js'),
    url('^people/$', 'people_iframe', name='widgets_people'),
    url('^test/$', 'test_widgets', name='widgets_test'),
)

    