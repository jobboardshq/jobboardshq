from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('zobpress.views',
    url(r'^$', 'index', name='zobpress_index'),
    url(r'^addjob/$', 'add_job', name='zobpress_add_job'),
    url(r'^categories/$', 'categories', name='zobpress_categories'),
    url(r'^jobs/$', 'jobs', name='zobpress_jobs'),
    #url(r'^job/(?P<id>\d+)/$', 'job', name='zobpress_job'),
    url(r'^job/(?P<job_slug>[\w\-]+)/$', 'job', name='zobpress_job'),
    url(r'^editjob/(?P<id>\d+)/$', 'edit_job', name='zobpress_edit_job'),
    url(r'^editjob/(?P<id>\d+)/done/$', 'edit_job_done', name='zobpress_edit_job_done'),
    url(r'^about/$', direct_to_template, {'template':'jobs/about.html'}, name='zobpress_about'),
    url(r'^create-page/$', 'create_page', name='zobpress_create_page'),
    
    
    #Categories
    url(r'^categories/jobs/(?P<category_slug>\w+)/$', 'category_jobs', name='zobpress_category_jobs'),
    
    #Feeds
    url(r'^feeds/jobs/$', 'feeds_jobs', name='zobpress_feeds_jobs'),
    
    #Paypal
    url(r'^job/(?P<id>\d+)/paypal/$', 'job_paypal', name='zobpress_jobs_paypal'),
    url(r'^job/(?P<id>\d+)/paypal/approved/$', 'job_paypal_approved', name='zobpress_jobs_paypal_appr'),
    
    
)