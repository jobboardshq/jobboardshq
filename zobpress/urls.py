from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('zobpress.views',
    # Example:
    url(r'^$', 'index', name='zobpress_index'),
    url(r'^addperson/$', 'add_person', name='zobpress_add_person'),
    url(r'^addjob/$', 'add_job', name='zobpress_add_job'),
    url(r'^persons/$', 'persons', name='zobpress_persons'),
    url(r'^jobs/$', 'jobs', name='zobpress_jobs'),
    url(r'^job/(?P<id>\d+)/$', 'job', name='zobpress_job'),
    url(r'^editjob/(?P<id>\d+)/$', 'edit_job', name='zobpress_edit_job'),
    url(r'^editjob/(?P<id>\d+)/done/$', 'edit_job_done', name='zobpress_edit_job_done'),
    url(r'^person/(?P<id>\d+)/$', 'person', name='zobpress_person'),
    url(r'^editperson/(?P<id>\d+)/$', 'edit_person', name='zobpress_edit_person'),
    url(r'^editdev/(?P<id>\d+)/done/$', 'edit_person_done', name='zobpress_edit_person_done'),
    url(r'^about/$', direct_to_template, {'template':'jobs/about.html'}, name='zobpress_about'),
    url(r'^create/jobform/$', 'create_job_form', name='zobpress_create_job_form'),
)