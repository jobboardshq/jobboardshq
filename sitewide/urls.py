from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('sitewide.views',
    url(r'^$', 'index', name='sitewide_index'),
    url(r'^features/$', direct_to_template, {"template":"sitewide/features.html"}, name='sitewide_features'),
    url(r'^demo/$', direct_to_template, {"template":"sitewide/demo.html"}, name='sitewide_demo'),
    url(r'^pricing/$', direct_to_template, {"template":"sitewide/pricing.html"}, name='sitewide_pricing'),
    url(r'^support/$', direct_to_template, {"template":"sitewide/support.html"}, name='sitewide_support'),
    url(r'^contact/$', direct_to_template, {"template":"sitewide/contact.html"}, name='sitewide_contact'),
    url(r'^register/$', 'register_board', name='sitewide_register_board'),
)

    