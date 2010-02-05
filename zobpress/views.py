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
from zobpress.models import type_mapping, JobFormModel, JobFieldModel, Job, BoardPayments,\
    JobType, DeletedEntities
from zobpress.models import Category, Job, Page
from zobpress.forms import get_job_form, JobStaticForm, PageForm, BoardSettingsForm, IndeedSearchForm, CategoryForm,\
    JobFieldEditForm, JobContactForm
from zobpress.decorators import ensure_has_board
from sitewide import views as sitewide_views
from django.forms.formsets import formset_factory
from django.forms.models import modelform_factory, modelformset_factory



def index(request):
    if not request.board:
        #We are at sidewide index.
        return sitewide_views.index(request)
    # list the jobs for the board
    return jobs(request)

@ensure_has_board
def add_job(request):
    "Add a job, via the backend."
    job_static_form = JobStaticForm(board = request.board, prefix = "job_static_form")
    job_contact_form = JobContactForm(prefix = "job_contact_form")
    Form = get_job_form(request.board,)
    form = Form( prefix = "form")
    if request.method == 'POST':
        form = Form(data = request.POST, files = request.FILES, prefix = "form")
        job_static_form = JobStaticForm(board = request.board, data = request.POST, prefix = "job_static_form")
        job_contact_form = JobContactForm(data = request.POST, prefix = "job_contact_form")
        if form.is_valid() and job_static_form.is_valid() and job_contact_form.is_valid():
            job = job_static_form.save()
            Form = get_job_form(request.board, job = job)
            form = Form(data = request.POST, files = request.FILES, prefix = "form")
            assert form.is_valid()
            form.save()
            contact = job_contact_form.save(commit = False)
            contact.job = job
            contact.board = request.board
            contact.save()
            request.user.message_set.create(message="The job has been added.")
            return HttpResponseRedirect(reverse('zobpress_index'))
    payload = {'form':form, 'job_static_form': job_static_form, "job_contact_form": job_contact_form}
    return render_to_response('zobpress/addjob.html', payload, RequestContext(request))

@ensure_has_board
def jobs(request):
    "Show a paginated list of jobs"
    try:
        order_by = request.GET['order']
    except:
        order_by = 'created_on'
    if order_by == 'created_on': order_by = '-created_on'
    if not order_by in ('name', 'created_on'):
        order_by = '-created_on'
    qs = models.Job.objects.filter().order_by(order_by)
    return object_list(request, template_name = 'zobpress/jobs.html', queryset = qs, template_object_name = 'jobs', paginate_by=10, extra_context={})
#
#@ensure_has_board
#def edit_job_old(request, id):
#    job = get_object_or_404(Job, id = id)    
#    if request.method == 'POST':
#        form = PasswordForm(request.POST)
#        if form.is_valid():
#            if form.cleaned_data['password'] == job.password:
#                request.session['job_edit_rights'] = id
#                return HttpResponseRedirect(('/editjob/%s/done/' % id))
#            else:
#                return HttpResponseForbidden('Wrong password. Go back and try again.')
#    if request.method == 'GET':
#        form = PasswordForm()
#    payload = {'form':form}
#    return render_to_response('zobpress/editjob.html', payload, RequestContext(request))


@ensure_has_board
def edit_job(request, id):
    "Edit job with given id."
    job = get_object_or_404(Job, board=request.board, id = id)
    job_static_form = JobStaticForm(board = request.board, instance = job)
    JobForm = get_job_form(request.board, job = job)
    if request.method == 'POST':
        form = JobForm(request.POST, files = request.FILES)
        if form.is_valid():
            job = form.save()
            return HttpResponseRedirect(job.get_absolute_url())
    elif request.method == 'GET':
        job = models.Job.objects.get(board = request.board, id = id)
        form = JobForm()
    payload = {'form': form, "job_static_form": job_static_form}
    return render_to_response('zobpress/editjob.html', payload, RequestContext(request))
    
@ensure_has_board
def category_jobs(request, category_slug):
    "Show jobs from a specific category."
    category = get_object_or_404(Category, board = request.board, slug = category_slug)
    jobs = Job.objects.filter(category = category)
    return object_list(request, queryset = jobs, template_name = 'zobpress/category_job_list.html', template_object_name = 'job')

@ensure_has_board
def categories(request):
    form = CategoryForm(board = request.board)
    categories = Category.objects.all()
    if request.method == "POST":
        form = CategoryForm(data = request.POST, board = request.board)
        if form.is_valid():
            category = form.save(commit = False)
            category.board = request.board
            category.save()
            request.user.message_set.create(message = "The category %s has been added." % category.name)
            return HttpResponseRedirect(".")
    extra = {"form": form}
    return object_list(request, queryset = categories, template_name = 'zobpress/categories.html', template_object_name = 'category', extra_context = extra)
        

@ensure_has_board
def edit_category(request, category_pk):
    category = get_object_or_404(Category, board = request.board, pk = category_pk)
    form = CategoryForm(instance = category, board = request.board)
    if request.method == "POST":
        form = CategoryForm(instance = category, data = request.POST, board = request.board)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(".")
    payload = dict(category=category, form=form)
    return render_to_response("zobpress/edit_category.html", payload, RequestContext(request))
    
    

@ensure_has_board
def feeds_jobs(request):
    "Show a RSS feed of jobs."
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

@ensure_has_board
def indeed_jobs(request):
    q = request.GET.get('q', '')
    l = request.GET['l']
    if not q or l:
        form = IndeedSearchForm()
        return render_to_response('zobpress/settings.html', {'form': form}, RequestContext(request))
    else:
        pass
        # TODO: query the indeed api parse the results & display.
        
@ensure_has_board
@login_required
def create_job_form_advanced(request):
    "Create a job form for a board."
    job_field_formset = modelformset_factory(JobFieldModel, fields=["name", "type", "required"])
    
    queryset = JobFieldModel.objects.filter(job_form__board = request.board)
    payload = {"job_field_formset": job_field_formset(queryset = queryset)}
    return render_to_response("zobpress/create_job_form_advanced.html", payload, RequestContext(request))

@ensure_has_board
def list_subscriptions(request):
    "Shows and allows actions for the list of subscribed users."
    from emailsubs.models import EmailSubscription
    subscriptions = EmailSubscription.objects.all()
    payload = {"subscriptions": subscriptions}
    if request.method ==  "POST":
        pass
        
        
    return render_to_response("zobpress/list_subscriptions.html", payload, RequestContext(request))

@ensure_has_board
def edit_page(request, page_slug):
    page = get_object_or_404(Page, page_slug = page_slug)
    form = PageForm(instance = page)
    if request.method == 'POST':
        form = PageForm(data = request.POST, instance = page)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message = "Page %s has been edited." % page.title)
            return HttpResponseRedirect(reverse("zobpress_job_board_page", args =[page.page_slug]))
    payload = {"form": form}
    return render_to_response("zobpress/edit_page.html", payload, RequestContext(request))
    
@ensure_has_board
def create_page(request):
    "Create a page for the board."
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.board = request.board
            page.save()
            request.user.message_set.create(message = "Page %s has been created." % page.title)
            return HttpResponseRedirect(reverse("zobpress_job_board_page", args =[page.page_slug]))
    else:
        form = PageForm()
    return render_to_response('zobpress/create_page.html', {'form': form}, RequestContext(request))

def trash(request):
    deleted = DeletedEntities.objects.all()
    deleted_objects =  [el.get_content_object() for el in deleted]
    payload = {"deleted": deleted, "deleted_objects":deleted_objects}
    return render_to_response('zobpress/trash.html', payload, RequestContext(request))

def untrash(request, pk):
    if request.method == "POST":
        deleted_object = DeletedEntities.objects.get(pk = pk)
        obj =  deleted_object.get_content_object()
        obj.is_deleted = False
        obj.save()
        deleted_object.delete()
        request.user.message_set.create(message = "You have undeleted %s." % obj)
        return HttpResponseRedirect(reverse("zobpress_trash"))
        


######Ajax views############

def delete_job(request, job_id):
    job = get_object_or_404(Job, pk = job_id)
    job.delete()
    payload = {"name": job.name, "pk": job.pk}
    return HttpResponse(simplejson.dumps(payload))

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk = category_id)
    category.delete()
    payload = {"name": category.name, "pk": category.pk}
    return HttpResponse(simplejson.dumps(payload))
    
def delete_job_type(request, job_id):
    job_type = get_object_or_404(JobType, pk = job_id)
    job_type.delete()
    payload = {"name": job_type.name, "pk": job_type.pk}
    return HttpResponse(simplejson.dumps(payload))


    
    
    

    
    
    
    
    
    
    
    