from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('frontend.views',
        url(r"^$", "index", name="frontend_index"),
        url(r"^addjob/$", "addjob", name="frontend_addjob"),
        url(r"^apply/(?P<job_slug>[\w-]+)$", "apply", name="frontend_apply"),   
        
        url(r'^job/(?P<job_slug>[\w\-]+)/$', 'job', name='frontend_job'),
        
        #Paypal
        url(r'^job/(?P<id>\d+)/paypal/$', 'job_paypal', name='frontend_job_paypal'),
        url(r'^job/(?P<id>\d+)/paypal/approved/$', 'job_paypal_approved', name='frontend_job_paypal_appr'),
           
        )

