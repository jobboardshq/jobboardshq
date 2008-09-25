from django.conf.urls.defaults import *

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^', include('zobpress.urls')),
    (r'^manage/', include('management.urls')),

    ('^admin/(.*)', admin.site.root),

)
