from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('zobpress.views',
    url(r'^$', 'index', name='zobpress_index'),
    url(r'^addjob/$', 'add_job', name='zobpress_add_job'),
    
    url(r'^categories/$', 'categories', name='zobpress_categories'),
    url(r'^category/edit/(?P<category_pk>\d+)/$', 'edit_category', name='zobpress_edit_category'),
    
    url(r'^job_types/$', 'job_types', name='zobpress_job_types'),
    #url(r'^job_types/$', 'job_types', name='zobpress_categories'),
    
    url(r'^jobs/$', 'jobs', name='zobpress_jobs'),
    url(r'^jobs/(?P<job_type_slug>[\w-]+)/$', 'jobs', name='zobpress_jobs_job_type'),
    #url(r'^job/(?P<id>\d+)/$', 'job', name='zobpress_job'),
    url(r'^jobform/advanced/$', 'create_job_form_advanced', name='zobpress_create_job_form_advanced'),
    url(r'^editjob/(?P<id>\d+)/$', 'edit_job', name='zobpress_edit_job'),
    #url(r'^editjob/(?P<id>\d+)/done/$', 'edit_job_done', name='zobpress_edit_job_done'),
    url(r'^about/$', direct_to_template, {'template':'jobs/about.html'}, name='zobpress_about'),
    url(r'^create-page/$', 'create_page', name='zobpress_create_page'),
    url(r'^subscriptions/$', 'list_subscriptions', name='zobpress_list_subscriptions'),
    url(r'^trash/$', 'trash', name='zobpress_trash'),
    url(r'^untrash/(?P<pk>\d+)/$', 'untrash', name='zobpress_untrash'),
    
    #Categories
    url(r'^categories/jobs/(?P<category_slug>[\w-]+)/$', 'category_jobs', name='zobpress_category_jobs'),
    
)

urlpatterns += patterns('zobpress.views',
        url(r'^ajax/delete/(?P<job_id>\d+)/$', 'delete_job', name='zobpress_delete_job'),
        url(r'^ajax/category-delete/(?P<category_id>\d+)/$', 'delete_category', name='zobpress_delete_category'),
        url(r'^ajax/type-delete/(?P<job_type_id>\d+)/$', 'delete_category', name='zobpress_delete_job_type'),
)                        

urlpatterns += patterns('zobpress.views',
    
    url(r'^edit/(?P<page_slug>.*)/$', 'edit_page', name='zobpress_job_board_page'),
    url(r'^create-page/$', 'create_page', name='zobpress_create_page'),
    url(r'^settings/$', 'settings', name='zobpress_settings'),
    url(r'^indeed-jobs/$', 'indeed_jobs', name='zobpress_indeed_jobs'),
)