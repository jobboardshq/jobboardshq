from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.contrib import admin
from django.conf import settings

from board_admin import board_admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^manage/', include('zobpress.urls')),
    (r'^', include('sitewide.urls')),
    (r'^optin/', include('emailsubs.urls')),
    #(r'^manage/', include('management.urls')),
    #(r'^widgets/', include('widgets.urls')),
    (r'^accounts/', include('registration.urls')),
    #(r'^', include('frontend.urls')),

    ("^admin/", include(admin.site.urls)),
    ('^boardadmin/(.*)', include(board_admin.urls) ),
    ('^404$', 'django.views.generic.simple.direct_to_template', {'template': 'tempaltes/404.html'}),
    ('^reg/$', 'django.views.generic.simple.direct_to_template', {'template': 'sitewide/landingpage.html'}),
    #(r'^search/', include('haystack.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, "show_indexes":True}, ),
    )
