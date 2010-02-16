from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from libs import paypal
from zobpress.decorators import ensure_has_board
from zobpress.models import Job, BoardPayments, Page
from zobpress.forms import JobStaticForm, JobContactForm, get_job_form

from haystack.views import SearchView
from haystack.forms import SearchForm
from frontend.forms import ApplyForm, AdvancedSearchForm
from django.utils import feedgenerator

@ensure_has_board
def index(request, category_slug = None, job_type_slug = None):
    board = request.board
    category = board.category_set.all()
    pages = board.page_set.all()
    jobs = board.job_set.all().filter(is_deleted = False)
    if category_slug:
        jobs = jobs.filter(category__slug = category_slug)
    if job_type_slug:
        jobs = jobs.filter(job_type__slug = job_type_slug)
    return render_to_response("frontend/index.html", {"category":category, "pages": pages, "jobs": jobs}, RequestContext(request))

@ensure_has_board
def addjob(request):
    board = request.board
    job_static_form = JobStaticForm(board = board, prefix="job_static_form")
    job_contact_form = JobContactForm(prefix="job_contact_form")
    JobForm = get_job_form(board = request.board)
    form = JobForm(prefix="form")
    if request.method == "POST":
        form = JobForm(data = request.POST, files = request.FILES, prefix = "form")
        job_static_form = JobStaticForm(board = request.board, data = request.POST, prefix = "job_static_form")
        job_contact_form = JobContactForm(data = request.POST, prefix = "job_contact_form")
        if form.is_valid() and job_static_form.is_valid() and job_contact_form.is_valid():
            job = job_static_form.save()
            Form = get_job_form(request.board, job = job)
            form = Form(data = request.POST, files = request.FILES,  prefix = "form")
            assert form.is_valid()
            form.save()
            contact = job_contact_form.save(commit = False)
            contact.job = job
            contact.board = request.board
            contact.save()
            #request.user.message_set.create(message="The job has been added.")
            #The job has been added. It is inactive yet. Ask user to pay via Paypal if needed.
            if not board.cost_per_job_listing:
                #There is no charge for adding Jobs to this board.
                job.is_active = True
                job.save()
                return HttpResponseRedirect(reverse("frontend_job", args=[job.job_slug]))
            else:
                return HttpResponseRedirect(reverse("frontend_job_paypal", args=[job.pk]))
            
    pages = board.page_set.all()
    payload = {"job_static_form": job_static_form, "job_contact_form": job_contact_form, "job_form": form, "pages": pages}
    return render_to_response("frontend/addjob.html", payload, RequestContext(request))


@ensure_has_board
def job(request, job_slug):
    "Show a specific job."
    board = request.board
    job = get_object_or_404(Job, board = board, job_slug=job_slug)
    job.times_viewed += 1
    job.save()
    pages = board.page_set.all()
    return render_to_response('frontend/job.html', {'job': job, "pages": pages}, RequestContext(request))

@ensure_has_board
def apply(request, job_slug):
    board = request.board
    job = get_object_or_404(Job, job_slug = job_slug)
    contact = job.primary_contact
    form = ApplyForm(board = request.board)
    if request.method == "POST":
        form = ApplyForm(board = request.board, data = request.POST, files = request.FILES)
        if form.is_valid():
            applicant = form.save(commit = False)
            applicant.board = request.board
            applicant.job = job
            applicant.save()
            return HttpResponseRedirect(reverse("frontend_apply_thanks",))
    
    pages = board.page_set.all() 
    payload = {"form": form, "contact":contact, "pages": pages}
    return render_to_response("frontend/apply.html", payload, RequestContext(request))


class BoardSearch(SearchView):
    def __call__(self, request):
        self.request = request
        
        self.form = self.build_form()
        self.query = self.get_query()
        results = super(BoardSearch, self).get_results()
        if results:
            self.results = results.filter(board = request.board)
        
        return self.create_response()
    
search = ensure_has_board(BoardSearch(form_class = SearchForm))

@ensure_has_board
def advanced_search(request):
    results = []
    search_performed = False
    if request.method == 'POST':
        form = AdvancedSearchForm(board=request.board, data=request.POST)
        if form.is_valid():
            from frontend.adv_search import search
            results = search(form.cleaned_data, request)
            search_performed = True
    else:
        form = AdvancedSearchForm(board=request.board)
    return render_to_response('frontend/advanced_search.html', {'form': form, 'results': results, 'search_performed': search_performed}, RequestContext(request))

@ensure_has_board
def feeds_jobs(request):
    "Show a RSS feed of jobs."
    board = request.board
    title = "Latest Jobs %s" % board.name
    link = reverse('frontend_feeds_jobs')
    description = "Latest Jobs added to our site %s" % board.name
    feed = feedgenerator.Atom1Feed(title = title, link = link, description = description)
    jobs = Job.objects.filter(board = board)
    for job in jobs:
        feed.add_item(title = job.name, link = job.get_absolute_url(), description=job.as_snippet())
    return HttpResponse(feed.writeString('UTF-8'))


@ensure_has_board
def job_board_pages(request, page_slug):
    "Show a page for a Board"
    board = request.board
    pages = board.page_set.all()
    page = get_object_or_404(Page, board=board, page_slug=page_slug)
    return render_to_response('frontend/static_pages.html', {'page': page, "pages": pages}, RequestContext(request))

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
    from django.conf import settings
    if settings.PAYPAL_DEBUG:
        pp = paypal.PayPal()
    else:
        pp = paypal.PayPal(api_endpoint = settings.API_ENDPOINT, paypal_url = settings.PAYPAL_URL, signature_values = settings.SIGNATURE_VALUES)
    token = pp.SetExpressCheckout(cost, '%s%s'%(board.get_absolute_url(), reverse('frontend_job_paypal_appr', args=[job.id])), '%s%s'%(board.get_absolute_url(), reverse('frontend_job_paypal', args=[job.id])))
    job.paypal_token_sec = token
    job.save()
    paypal_url = pp.PAYPAL_URL + token
    pages = board.page_set.all()
    payload = {'job':job, 'paypal_url':paypal_url, "pages": pages}
    return render_to_response('frontend/job_paypal.html', payload, RequestContext(request))

@ensure_has_board
def job_paypal_approved(request, id):
    board = request.board
    cost = board.cost_per_job_listing
    job = get_object_or_404(Job, id = id)
    if job.is_active:
        return HttpResponseRedirect(job.get_absolute_url())
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
    payload['pages'] = board.page_set.all()
    return render_to_response('frontend/job_paypal_approved.html', payload, RequestContext(request))

