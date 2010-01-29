from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('frontend.views',
        url(r"^$", "index", name="frontend_index"),
        url(r"^addjob/$", "addjob", name="frontend_addjob"),
        url(r"^apply/(?P<job_slug>[\w-]+)$", "apply", name="frontend_apply"),      
        )

