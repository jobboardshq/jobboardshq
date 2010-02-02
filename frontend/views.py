from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from libs import paypal
from zobpress.decorators import ensure_has_board
from zobpress.models import Job, BoardPayments
from zobpress.forms import JobStaticForm, JobContactForm, get_job_form

from haystack.views import SearchView
from haystack.forms import SearchForm

@ensure_has_board
def index(request, category_slug = None, job_type_slug = None):
    board = request.board
    category = board.category_set.all()
    pages = board.page_set.all()
    jobs = board.job_set.all()
    if category_slug:
        jobs = jobs.filter(category__slug = category_slug)
    if job_type_slug:
        jobs = jobs.filter(job_type__slug = category_slug)
    return render_to_response("frontend/index.html", {"category":category, "pages": pages, "jobs": jobs}, RequestContext(request))

@ensure_has_board
def addjob(request):
    board = request.board
    job_static_form = JobStaticForm(board = board)
    job_contact_form = JobContactForm()
    JobForm = get_job_form(board = request.board)
    form = JobForm()
    if request.method == "POST":
        form = JobForm(data = request.POST, files = request.FILES)
        job_static_form = JobStaticForm(board = request.board, data = request.POST)
        job_contact_form = JobContactForm(data = request.POST)
        if form.is_valid() and job_static_form.is_valid() and job_contact_form.is_valid():
            job = job_static_form.save()
            Form = get_job_form(request.board, job = job)
            form = Form(data = request.POST, files = request.FILES)
            assert form.is_valid()
            form.save()
            contact = job_contact_form.save(commit = False)
            contact.job = job
            contact.board = request.board
            contact.save()
            request.user.message_set.create(message="The job has been added.")
            #The job has been added. It is inactive yet. Ask user to pay via Paypal if needed.
            if not board.cost_per_job_listing:
                #There is no charge for adding Jobs to this board.
                job.is_active = True
                job.save()
                return HttpResponseRedirect(reverse("frontend_job", args=[job.job_slug]))
            else:
                return HttpResponseRedirect(reverse("frontend_job_paypal", args=[job.pk]))
            
        
    payload = {"job_static_form": job_static_form, "job_contact_form": job_contact_form, "job_form": form}
    return render_to_response("frontend/addjob.html", payload, RequestContext(request))


@ensure_has_board
def job(request, job_slug):
    "Show a specific job."
    board = request.board
    job = get_object_or_404(Job, board = board, job_slug=job_slug)
    job.times_viewed += 1
    job.save()
    return render_to_response('frontend/job.html', {'job': job}, RequestContext(request))

@ensure_has_board
def apply(request, job_slug):
    pass


class BoardSearch(SearchView):
    def __call__(self, request):
        self.request = request
        
        self.form = self.build_form()
        self.query = self.get_query()
        results = super(BoardSearch, self).get_results()
        self.results = results.filter(board = request.board)
        
        return self.create_response()
    
search = ensure_has_board(BoardSearch(form_class = SearchForm))
        
        
    


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
    token = pp.SetExpressCheckout(cost, '%s%s'%(board.get_absolute_url(), reverse('frontend_job_paypal_appr', args=[job.id])), '%s%s'%(board.get_absolute_url(), reverse('frontend_job_paypal', args=[job.id])))
    job.paypal_token_sec = token
    job.save()
    paypal_url = pp.PAYPAL_URL + token
    payload = {'job':job, 'paypal_url':paypal_url}
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
    return render_to_response('frontend/job_paypal_approved.html', payload, RequestContext(request))

