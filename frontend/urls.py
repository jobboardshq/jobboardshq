from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template




urlpatterns = patterns('frontend.views',
        url(r"^$", "index", name="frontend_index"),
        url(r"^category/(?P<category_slug>[\w-]+)/$", "index", name="frontend_category_jobs"),
        url(r"^type/(?P<job_type_slug>[\w-]+)/$", "index", name="frontend_job_type_jobs"),
        
        url(r"^addjob/$", "addjob", name="frontend_addjob"),
        
        url(r"^apply/done/$", direct_to_template, {"template": "frontend/apply_done.html"}, name="frontend_apply_thanks"),
        url(r"^apply/(?P<job_slug>[\w-]+)/$", "apply", name="frontend_apply"),   
        
        url(r'^job/(?P<job_slug>[\w\-]+)/$', 'job', name='frontend_job'),
        
        #Paypal
        url(r'^job/(?P<id>\d+)/paypal/$', 'job_paypal', name='frontend_job_paypal'),
        url(r'^job/(?P<id>\d+)/paypal/approved/$', 'job_paypal_approved', name='frontend_job_paypal_appr'),
        
        url(r'^pages/(?P<page_slug>.*)/$', 'job_board_pages', name='frontend_job_board_page'),
        
        url(r'^search/$', "search", name='frontend_search'),
        url(r'^advanced-search/$', "advanced_search", name='frontend_advanced_search'),
        
        #Feeds
        url(r'^feeds/jobs/$', 'feeds_jobs', name='frontend_feeds_jobs'),
           
        )

