from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('zobpress.views',
    url(r'^$', 'index', name='zobpress_index'),
    url(r'^addjob/$', 'add_job', name='zobpress_add_job'),
    
    url(r'^categories/$', 'categories', name='zobpress_categories'),
    url(r'^category/edit/(?P<category_pk>\d+)/$', 'edit_category', name='zobpress_edit_category'),
    
    url(r'^jobs/$', 'jobs', name='zobpress_jobs'),
    #url(r'^job/(?P<id>\d+)/$', 'job', name='zobpress_job'),
    url(r'^jobform/advanced/$', 'create_job_form_advanced', name='zobpress_create_job_form_advanced'),
    url(r'^editjob/(?P<id>\d+)/$', 'edit_job', name='zobpress_edit_job'),
    #url(r'^editjob/(?P<id>\d+)/done/$', 'edit_job_done', name='zobpress_edit_job_done'),
    url(r'^about/$', direct_to_template, {'template':'jobs/about.html'}, name='zobpress_about'),
    url(r'^create-page/$', 'create_page', name='zobpress_create_page'),
    url(r'^subscriptions/$', 'list_subscriptions', name='zobpress_list_subscriptions'),
    
    
    #Categories
    url(r'^categories/jobs/(?P<category_slug>\w+)/$', 'category_jobs', name='zobpress_category_jobs'),
    
    #Feeds
    url(r'^feeds/jobs/$', 'feeds_jobs', name='zobpress_feeds_jobs'),
    
    
    
)