from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import feedgenerator

from zobpress.models import Job

def index(request):
    widget_code = str(render_to_string('widgets/widget_code.html', RequestContext(request)))
    return render_to_response('widgets/index.html', {'widget_code': widget_code}, RequestContext(request))

def jobs_js(request):
    payload = {}
    return render_to_response('widgets/jobs.js', payload, RequestContext(request), mimetype='text/javascript',)

def jobs_iframe(request):
    jobs = Job.objects.all()[:10]
    payload = {'jobs':jobs}
    return render_to_response('widgets/jobs.html', payload, RequestContext(request))
    
def test_widgets(request):
    payload = {}
    return render_to_response('widgets/test.html', payload, RequestContext(request))
    
