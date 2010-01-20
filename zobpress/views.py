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
from zobpress.models import Category, Job, Page
from zobpress.forms import get_job_form, PasswordForm, JobStaticForm, PageForm, BoardSettingsForm, IndeedSearchForm, CategoryForm
from zobpress.decorators import ensure_has_board
from libs import paypal
from sitewide import views as sitewide_views



def index(request):
    if not request.board:
        #We are at sidewide index.
        return sitewide_views.index(request)
    # list the jobs for the board
    return jobs(request)

@ensure_has_board
def add_job(request):
    job_static_form = JobStaticForm(board = request.board)
    password_form = PasswordForm()
    Form = get_job_form(request.board)
    if request.method == 'POST':
        form = Form(data = request.POST, files = request.FILES)
        job_static_form = JobStaticForm(board = request.board, data = request.POST)
        if form.is_valid() and job_static_form.is_valid():
            object = form.save()
            object.name = job_static_form.cleaned_data['name']
            object.save()
            password_form = PasswordForm(data = request.POST)
            if password_form.is_valid():
                object.is_editable = True
                object.password = password_form.save()
                object.save()
            #return HttpResponseRedirect(object.get_absolute_url())
            job = object    
            return HttpResponseRedirect(reverse('zobpress_jobs_paypal', args=[job.id]))
    else:
        form = Form()
    payload = {'form':form, 'job_static_form': job_static_form, 'password_form':password_form}
    return render_to_response('zobpress/addjob.html', payload, RequestContext(request))

@ensure_has_board
def job(request, job_slug):
    # qs = models.Job.objects.filter(is_active = True)
    job = get_object_or_404(Job, job_slug=job_slug)
    return render_to_response('zobpress/job.html', {'job': job}, RequestContext(request))

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
    return object_list(request, template_name = 'zobpress/jobs.html', queryset = qs, template_object_name = 'jobs', paginate_by=10, extra_context={})

@ensure_has_board
def edit_job(request, id):
    job = get_object_or_404(Job, id = id)    
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
    return render_to_response('zobpress/editjob.html', payload, RequestContext(request))

@ensure_has_board
def edit_job_done(request, id):
    job = get_object_or_404(Job, id = id)
    job_static_form = JobStaticForm(board = request.board)
    JobForm = get_job_form(request.board, job = job)
    if request.method == 'POST':
        form = JobForm(request.POST, files = request.FILES)
        if form.is_valid():
            job = form.save()
            return HttpResponseRedirect(job.get_absolute_url())
    elif request.method == 'GET':
        job = models.Job.objects.get(id = id)
        form = JobForm()
    payload = {'form': form, "job_static_form": job_static_form}
    return render_to_response('zobpress/editjob.html', payload, RequestContext(request))
    
@ensure_has_board
def category_jobs(request, category_slug):
    category = get_object_or_404(Category, slug = category_slug)
    jobs = Job.objects.filter(category = category)
    return object_list(request, queryset = jobs, template_name = 'zobpress/category_job_list.html', template_object_name = 'job')

@ensure_has_board
def categories(request):
    form = CategoryForm()
    categories = Category.objects.all()
    if request.method == "POST":
        form = CategoryForm(data = request.POST)
        if form.is_valid():
            category = form.save(commit = False)
            category.board = request.board
            category.save()
        return HttpResponseRedirect(reverse("zobpress_index"))
    extra = {"form": form}
    return object_list(request, queryset = categories, template_name = 'zobpress/categories.html', template_object_name = 'category', extra_context = extra)
        
            
    

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
def job_paypal(request, id):
    board = request.board
    job = get_object_or_404(Job, id = id)
    cost = board.cost_per_job_listing
    if job.is_active:
        raise Http404#Already paid for, get outa here.
    if cost == 0:#No cost. Set active and redirect.
        job.is_active = True
        job.save()
        return HttpResponseRedirect(job.get_absolute_url())
    pp = paypal.PayPal()
    token = pp.SetExpressCheckout(cost, '%s%s'%(board.get_absolute_url(), reverse('zobpress_jobs_paypal_appr', args=[job.id])), '%s%s'%(board.get_absolute_url(), reverse('zobpress_jobs_paypal', args=[job.id])))
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

@ensure_has_board
def job_board_pages(request, page_slug):
    board = request.board
    page = get_object_or_404(Page, job_board=board, page_slug=page_slug)
    return render_to_response('zobpress/static_pages.html', {'page': page}, RequestContext(request))

@ensure_has_board
def create_page(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.job_board = request.board
            page.save()
            return HttpResponseRedirect('/pages/%s/' %(form.cleaned_data['page_slug']))
    else:
        form = PageForm()
    return render_to_response('zobpress/create_page.html', {'form': form}, RequestContext(request))

@ensure_has_board
def settings(request):
    if request.method == 'POST':
        form = BoardSettingsForm(request.POST, instance=request.board.settings)
        board_settings = form.save(commit=False)
        board_settings.board = request.board
        board_settings.save()
        HttpResponseRedirect(reverse('zobpress_settings'))
    else:
        form = BoardSettingsForm(instance=request.board.settings)
    return render_to_response('zobpress/settings.html', {'form': form}, RequestContext(request))

def indeed_jobs(request):
    q = request.GET.get('q', '')
    l = request.GET['l']
    if not q or l:
        form = IndeedSearchForm()
        return render_to_response('zobpress/settings.html', {'form': form}, RequestContext(request))
    else:
        pass
        # TODO: query the indeed api parse the results & display.