from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('management.views',
    url(r'^$', 'index', name='manage_index'),
    url(r'^create/jobform/$', 'create_job_form', name='manage_create_job_form'),
    url(r'^create/personform/$', 'create_person_form', name='manage_create_person_form'),

)

    