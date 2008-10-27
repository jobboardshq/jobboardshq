from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from StringIO import StringIO

from zobpress import models
from zobpress.models import type_mapping, JobFormModel, JobFieldModel
from zobpress.forms import get_job_form, get_employee_form, PasswordForm
from django.utils import simplejson

def index(request):
    return add_person(request)

def handle_form(request, Form, template_name):
    if request.method == 'POST':
        form = Form(data = request.POST)
        if form.is_valid():
            object = form.save()
            return HttpResponseRedirect(object.get_absolute_url())
    if request.method == 'GET':
        form = Form()
    payload = {'form':form}
    return render_to_response(template_name, payload)

def add_person(request):
    EmployeeForm = get_employee_form(request.board)
    return handle_form(request, EmployeeForm, 'zobpress/addperson.html')

def add_job(request):
    JobForm = get_job_form(request.board)
    return handle_form(request, JobForm, 'zobpress/addjob.html')

def person(request, id):
    qs = models.Employee.objects.all()
    return object_detail(request, template_name = 'zobpress/person.html', queryset = qs, object_id = id, template_object_name = 'person')
    
def job(request, id):
    qs = models.Job.objects.all()
    return object_detail(request, template_name = 'zobpress/job.html', queryset = qs, object_id = id, template_object_name = 'job')

def persons(request):
    try:
        order_by = request.GET['order']
    except:
        order_by = 'created_on'
    if order_by == 'created_on': order_by = '-created_on'
    if not order_by in ('name', 'created_on'):
        order_by = '-created_on'        
    qs = models.Employee.objects.all().order_by(order_by)
    return object_list(request, template_name = 'zobpress/persons.html', queryset = qs, template_object_name = 'developers', paginate_by=10)

def jobs(request):
    try:
        order_by = request.GET['order']
    except:
        order_by = 'created_on'
    if order_by == 'created_on': order_by = '-created_on'
    if not order_by in ('name', 'created_on'):
        order_by = '-created_on'
    qs = models.Job.objects.all().order_by(order_by)
    return object_list(request, template_name = 'zobpress/jobs.html', queryset = qs, template_object_name = 'jobs', paginate_by=10)

def edit_job(request, id):
    job = models.Job.objects.get(id = id)
    if not job.is_editable:
        raise Http404
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == job.password:
                request.session['job_edit_rights'] = id
                return HttpResponseRedirect(('/editjob/%s/done/' % id))
            else:
                return HttpResponseForbidden('Wrong password. Go back and try again.')
    if request.method == 'GET':
        form = PasswordForm()
    payload = {'form':form}
    return render_to_response('zobpress/editjob.html', payload)

def edit_person(request, id):
    dev = models.Developer.objects.get(id = id)
    if not dev.is_editable:
        raise Http404    
    if request.method == 'POST':
        form = PasswordForm(request.POST)        
        if form.is_valid():
            if form.cleaned_data['password'] == dev.password:
                request.session['dev_edit_rights'] = id
                return HttpResponseRedirect(('/editdev/%s/done/' % id))
            else:
                return HttpResponseForbidden('Wrong password. Go back and try again.')
    if request.method == 'GET':
        form = PasswordForm()
    payload = {'form':form}
    return render_to_response('zobpress/editperson.html', payload)

def edit_job_done(request, id):
    job = models.Job.objects.get(id = id)
    if not job.is_editable:
        raise Http404    
    if request.method == 'POST':
        form = JobForm(request.POST, instance = job)
        if form.is_valid():
            job = form.save()
            return HttpResponseRedirect(job.get_absolute_url())
    elif request.method == 'GET':
        job = models.Job.objects.get(id = id)
        form = JobForm(instance = job)
    payload = {'form': form}
    return render_to_response('zobpress/editjob.html', payload)
    
def edit_person_done(request, id):
    dev = models.Developer.objects.get(id = id)
    if not dev.is_editable:
        raise Http404    
    if request.method == 'POST':
        form = DeveloperForm(request.POST, instance = dev)
        if form.is_valid():
            dev = form.save()
            return HttpResponseRedirect(dev.get_absolute_url())
    elif request.method == 'GET':
        dev = models.Developer.objects.get(id = id)
        form = DeveloperForm(instance = dev)
    payload = {'form': form}
    return render_to_response('zobpress/adddev.html', payload)

def create_job_form(request):
    "Create a job form for a board."
    if request.method == 'POST' and request.is_ajax():
        data = simplejson.load(StringIO(request.POST['data']))
        job_form, created = JobFormModel.objects.get_or_create(board = request.board)
        job_form.jobfieldmodel_set.all().delete()
        order = 1
        for field in data:
            field_obj = JobFieldModel(job_form = job_form, name = field[0], type=field[1], order = order)
            order += 1
            field_obj.save()
            success_url = reverse('zobpress_add_job')
            return HttpResponse(success_url)
    payload = {}
    return render_to_response('zobpress/create_form.html', payload, RequestContext(request))
