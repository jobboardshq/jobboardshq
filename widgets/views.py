from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import feedgenerator

from zobpress.models import Job, Employee

def jobs_js(request):
    payload = {}
    return render_to_response('widgets/jobs.js', payload, RequestContext(request), mimetype='text/javascript',)

def jobs_iframe(request):
    jobs = Job.objects.all()[:10]
    payload = {'jobs':jobs}
    return render_to_response('widgets/jobs.html', payload, RequestContext(request))
    
def people_js(request):
    payload = {}
    return render_to_response('widgets/people.js', payload, RequestContext(request), mimetype='text/javascript')

def people_iframe(request):
    employees = Employee.objects.all()[:10]
    payload = {'employees':employees}
    return render_to_response('widgets/people.html', payload, RequestContext(request))

def test_widgets(request):
    payload = {}
    return render_to_response('widgets/test.html', payload, RequestContext(request))
    
