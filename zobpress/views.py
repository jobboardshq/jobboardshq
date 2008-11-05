from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import feedgenerator
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from StringIO import StringIO

from zobpress import models
from zobpress.models import type_mapping, JobFormModel, JobFieldModel, Job, BoardPayments
from zobpress.models import EmployeeFormModel, EmployeeFieldModel, Category, Employee
from zobpress.forms import get_job_form, get_employee_form, PasswordForm
from zobpress.decorators import ensure_has_board
from libs import paypal
from sitewide import views as sitewide_views


def index(request):
    if not request.board:
        #We are at sidewide index.
        return sitewide_views.index(request)
    return add_person(request)

def handle_form(request, Form, template_name, do_redirect = True):
    password_form = PasswordForm()
    if request.method == 'POST':
        form = Form(data = request.POST, files = request.FILES)
        if form.is_valid():
            object = form.save()
            password_form = PasswordForm(data = request.POST)
            if password_form.is_valid():
                object.is_editable = True
                object.password = password_form.save()
                object.save()
            if do_redirect:
                return HttpResponseRedirect(object.get_absolute_url())
            else:
                return object
    if request.method == 'GET':
        form = Form()
    payload = {'form':form, 'password_form':password_form}
    return render_to_response(template_name, payload, RequestContext(request))

@ensure_has_board
def add_person(request):
    EmployeeForm = get_employee_form(request.board)
    if request.method == 'POST':
        employee = handle_form(request, EmployeeForm, 'zobpress/addperson.html', do_redirect = False)    
        return HttpResponseRedirect(reverse('zobpress_persons_paypal', args=[employee.id]))
    return handle_form(request, EmployeeForm, 'zobpress/addperson.html', do_redirect = False)

@ensure_has_board
def add_job(request):
    JobForm = get_job_form(request.board)
    if request.method == 'POST':
        job = handle_form(request, JobForm, 'zobpress/addjob.html', do_redirect = False)    
        return HttpResponseRedirect(reverse('zobpress_jobs_paypal', args=[job.id]))
    return handle_form(request, JobForm, 'zobpress/addjob.html')

@ensure_has_board
def person(request, id):
    qs = models.Employee.public_objects.get_public_employees(board = request.board)
    return object_detail(request, template_name = 'zobpress/person.html', queryset = qs, object_id = id, template_object_name = 'person')
    
@ensure_has_board
def job(request, id):
    qs = models.Job.objects.filter(is_active = True)
    return object_detail(request, template_name = 'zobpress/job.html', queryset = qs, object_id = id, template_object_name = 'job')

@ensure_has_board
def persons(request):
    try:
        order_by = request.GET['order']
    except:
        order_by = 'created_on'
    if order_by == 'created_on': order_by = '-created_on'
    if not order_by in ('name', 'created_on'):
        order_by = '-created_on'        
    qs = models.Employee.objects.filter(is_active = True).order_by(order_by)
    return object_list(request, template_name = 'zobpress/persons.html', queryset = qs, template_object_name = 'developers', paginate_by=10)

@ensure_has_board
def jobs(request):
    try:
        order_by = request.GET['order']
    except:
        order_by = 'created_on'
    if order_by == 'created_on': order_by = '-created_on'
    if not order_by in ('name', 'created_on'):
        order_by = '-created_on'
    qs = models.Job.objects.filter(is_active = True).order_by(order_by)
    return object_list(request, template_name = 'zobpress/jobs.html', queryset = qs, template_object_name = 'jobs', paginate_by=10)

@ensure_has_board
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

@ensure_has_board
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

@ensure_has_board
def edit_job_done(request, id):
    job = models.Job.objects.get(id = id)
    JobForm = get_job_form(request.board, job = job)
    if not job.is_editable:
        raise Http404    
    if request.method == 'POST':
        form = JobForm(request.POST, files = request.FILES)
        if form.is_valid():
            job = form.save()
            return HttpResponseRedirect(job.get_absolute_url())
    elif request.method == 'GET':
        job = models.Job.objects.get(id = id)
        form = JobForm()
    payload = {'form': form}
    return render_to_response('zobpress/editjob.html', payload)
    
@ensure_has_board
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

@ensure_has_board
@login_required
def create_job_form(request):
    "Create a job form for a board."
    if not request.user == request.board.owner:
        return HttpResponseForbidden('You do not have access to this board')
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
    return render_to_response('zobpress/create_job_form.html', payload, RequestContext(request))

@ensure_has_board
@login_required
def create_person_form(request):
    "Create a person form for a board."
    if not request.user == request.board.owner:
        return HttpResponseForbidden('You do not have access to this board')
    if request.method == 'POST' and request.is_ajax():
        data = simplejson.load(StringIO(request.POST['data']))
        employee_form, created = EmployeeFormModel.objects.get_or_create(board = request.board)
        employee_form.employeefieldmodel_set.all().delete()
        order = 1
        for field in data:
            field_obj = EmployeeFieldModel(employee_form = employee_form, name = field[0], type=field[1], order = order)
            order += 1
            field_obj.save()
        success_url = reverse('zobpress_add_person')
        return HttpResponse(success_url)
    payload = {}
    return render_to_response('zobpress/create_person_form.html', payload, RequestContext(request))

@ensure_has_board
def category_jobs(request, category_slug):
    category = get_object_or_404(Category, slug = category_slug)
    jobs = Job.objects.filter(category = category)
    return object_list(request, queryset = jobs, template_name = 'zobpress/category_job_list.html', template_object_name = 'job')

@ensure_has_board
def category_persons(request, category_slug):
    category = get_object_or_404(Category, slug = category_slug)
    employees = Employee.objects.filter(category = category)
    return object_list(request, queryset = employees, template_name = 'zobpress/category_employee_list.html', template_object_name = 'employee')

@ensure_has_board
def feeds_jobs(request):
    board = request.board
    title = "Latest Jobs %s" % board.name
    link = reverse('zobpress_feeds_jobs')
    description = "Latest Jobs added to our site %s" % board.name
    feed = feedgenerator.Atom1Feed(title = title, link = link, description = description)
    jobs = Job.objects.filter(board = board)
    for job in jobs:
        feed.add_item(title = job.name, link = job.get_absolute_url(), description=job.as_snippet())
    return HttpResponse(feed.writeString('UTF-8'))

@ensure_has_board
def feeds_people(request):
    board = request.board
    title = "Recently added people %s" % board.name
    link = reverse('zobpress_feeds_people')
    description = "People recently added to our site %s" % board.name
    feed = feedgenerator.Atom1Feed(title = title, link = link, description = description)
    employees = Employee.objects.filter(board = board)
    for employee in employees:
        feed.add_item(title = employee.name, link = employee.get_absolute_url(), description=employee.as_snippet())
    return HttpResponse(feed.writeString('UTF-8'))

@ensure_has_board
def person_paypal(request, id):
    board = request.board
    person = get_object_or_404(Employee, id = id)
    cost = board.cost_per_people_listing
    if person.is_active:
        raise Http404#Already paid for, get outa here.
    if cost == 0:#No cost. Set active and redirect.
        person.is_active = True
        person.save()
        return HttpResponseRedirect(person.get_absolute_url())
    pp = paypal.PayPal()
    token = pp.SetExpressCheckout(cost, '%s%s'%(board.get_absolute_url(), reverse('zobpress_persons_paypal_appr', args=[person.id])), '%s%s'%(board.get_absolute_url(), reverse('zobpress_persons_paypal', args=[person.id])))
    person.paypal_token_sec = token
    person.save()
    paypal_url = pp.PAYPAL_URL + token
    payload = {'person':person, 'paypal_url':paypal_url}
    return render_to_response('zobpress/person_paypal.html', payload, RequestContext(request))

@ensure_has_board
def person_paypal_approved(request, id):
    board = request.board
    cost = board.cost_per_people_listing
    person = get_object_or_404(Employee, id = id, is_active = False)
    pp = paypal.PayPal()
    paypal_details = pp.GetExpressCheckoutDetails(person.paypal_token_sec, return_all = True)
    payload = {'person':person}
    if 'Success' in paypal_details['ACK']:
        payload['ack'] = True
        token = paypal_details['TOKEN'][0]
        first_name = paypal_details['FIRSTNAME'][0]
        last_name = paypal_details['LASTNAME'][0]
        amt = paypal_details['AMT'][0]
        payer_id = request.GET['PayerID']
        payload_update  = {'first_name':first_name, 'last_name':last_name, 'amt':amt}
        payload.update(payload_update)
        payment_details  = pp.DoExpressCheckoutPayment(token = token, payer_id = payer_id, amt = cost)
        if 'Success' in payment_details['ACK']:
            person.is_active = True
            person.save()
            BoardPayments.objects.add_employee_payments(board = board, amount = cost)
        else:
            payload['ack'] = False
    else:
        payload['ack'] = False
    return render_to_response('zobpress/person_paypal_approved.html', payload, RequestContext(request))
    
@ensure_has_board
def job_paypal(request, id):
    board = request.board
    job = get_object_or_404(Job, id = id)
    cost = board.cost_per_job_listing
    if job.is_active:
        raise Http404#Already paid for, get outa here.
    if cost == 0:#No cost. Set active and redirect.
        job.is_active = True
        job.save()
        return HttpResponseRedirect(person.get_absolute_url())
    pp = paypal.PayPal()
    token = pp.SetExpressCheckout(cost, '%s%s'%(board.get_absolute_url(), reverse('zobpress_jobs_paypal_appr', args=[job.id])), '%s%s'%(board.get_absolute_url(), reverse('zobpress_persons_paypal', args=[job.id])))
    job.paypal_token_sec = token
    job.save()
    paypal_url = pp.PAYPAL_URL + token
    payload = {'job':job, 'paypal_url':paypal_url}
    return render_to_response('zobpress/job_paypal.html', payload, RequestContext(request))

@ensure_has_board
def job_paypal_approved(request, id):
    board = request.board
    cost = board.cost_per_people_listing
    job = get_object_or_404(Job, id = id, is_active = False)
    pp = paypal.PayPal()
    paypal_details = pp.GetExpressCheckoutDetails(job.paypal_token_sec, return_all = True)
    payload = {'job':job}
    if 'Success' in paypal_details['ACK']:
        payload['ack'] = True
        token = paypal_details['TOKEN'][0]
        first_name = paypal_details['FIRSTNAME'][0]
        last_name = paypal_details['LASTNAME'][0]
        amt = paypal_details['AMT'][0]
        payer_id = request.GET['PayerID']
        payload_update  = {'first_name':first_name, 'last_name':last_name, 'amt':amt}
        payload.update(payload_update)
        payment_details  = pp.DoExpressCheckoutPayment(token = token, payer_id = payer_id, amt = cost)
        if 'Success' in payment_details['ACK']:
            job.is_active = True
            job.save()
            BoardPayments.objects.add_job_payment(board = board, amount = cost)
        else:
            payload['ack'] = False
    else:
        payload['ack'] = False
    return render_to_response('zobpress/person_paypal_approved.html', payload, RequestContext(request))

