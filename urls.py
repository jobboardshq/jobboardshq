from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.conf import settings

from board_admin import board_admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^manage/', include('zobpress.urls')),
    (r'^sitewide/', include('sitewide.urls')),
    (r'^optin/', include('emailsubs.urls')),
    (r'^manage/', include('management.urls')),
    (r'^widgets/', include('widgets.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^', include('frontend.urls')),

    ('^admin/(.*)', admin.site.root),
    ('^boardadmin/(.*)', board_admin.root),
    #(r'^search/', include('haystack.urls')),
)



if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, "show_indexes":True}, ),
    )
