from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('frontend.views',
        url(r"^$", "index", name="frontent_index"),
        url(r"^addjob/$", "addjob", name="frontent_addjob"),
        url(r"^subscribe/$", "subscribe", name="frontent_subscribe"),
        url(r"^apply/(?P<job_slug>[\w-]+)$", "apply", name="frontent_apply"),      
        )

