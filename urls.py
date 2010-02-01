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
    (r'^search/', include('haystack.urls')),
)

urlpatterns += patterns('zobpress.views',
    url(r'^pages/(?P<page_slug>.*)/$', 'job_board_pages', name='zobpress_job_board_page'),
    # url(r'^edit/(?P<page_slug>.*)/$', 'edit_pages', name='zobpress_edit_page'),
    url(r'^create-page/$', 'create_page', name='zobpress_create_page'),
    url(r'^settings/$', 'settings', name='zobpress_settings'),
    url(r'^indeed-jobs/$', 'indeed_jobs', name='zobpress_indeed_jobs'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, "show_indexes":True}, ),
    )
