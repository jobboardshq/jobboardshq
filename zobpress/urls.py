from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('zobpress.views',
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
    
    #Categories
    url(r'^categories/jobs/(?P<category_slug>\w+)/$', 'category_jobs', name='zobpress_category_jobs'),
    url(r'^categories/persons/(?P<category_slug>\w+)/$', 'category_persons', name='zobpress_category_persons'),
    
    #Feeds
    url(r'^feeds/jobs/$', 'feeds_jobs', name='zobpress_feeds_jobs'),
    url(r'^feeds/people/$', 'feeds_people', name='zobpress_feeds_people'),
    
    #Paypal
    url(r'^person/(?P<id>\d+)/paypal/$', 'person_paypal', name='zobpress_persons_paypal'),
    url(r'^person/(?P<id>\d+)/paypal/aproved/$', 'person_paypal_approved', name='zobpress_persons_paypal_appr'),
    url(r'^job/(?P<id>\d+)/paypal/$', 'job_paypal', name='zobpress_jobs_paypal'),
    url(r'^job/(?P<id>\d+)/paypal/approved/$', 'job_paypal_approved', name='zobpress_jobs_paypal_appr'),
    
    
)