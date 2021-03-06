from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('management.views',
    url(r'^$', 'index', name='manage_index'),
    url(r'^upgrade/$', 'upgrade', name='manage_upgrade'),
    url(r'^upgrade/approved/$', 'upgrade_approved', name='manage_board_paypal_appr'),
    url(r'^create/jobform/$', 'create_job_form', name='manage_create_job_form'),
)

    