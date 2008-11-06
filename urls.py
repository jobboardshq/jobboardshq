from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from board_admin import board_admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^', include('zobpress.urls')),
    (r'^sitewide/', include('sitewide.urls')),
    (r'^optin/', include('emailsubs.urls')),
    (r'^manage/', include('management.urls')),
    (r'^widgets/', include('widgets.urls')),
    (r'^accounts/', include('registration.urls')),

    ('^admin/(.*)', admin.site.root),
    ('^boardadmin/(.*)', board_admin.root),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
