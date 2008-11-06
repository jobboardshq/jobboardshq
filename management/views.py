from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.conf import settings

from StringIO import StringIO

from management.forms import ManageSettingsForm
from zobpress.decorators import ensure_has_board
from zobpress.models import type_mapping, JobFormModel, JobFieldModel, Job, BoardPayments
from zobpress.models import EmployeeFormModel, EmployeeFieldModel, Category, Employee, BoardPayPal
from libs import paypal

@ensure_has_board
@login_required
def index(request):
    if not request.user == request.board.owner:
        return HttpResponseForbidden('You do not have access to this board')
    manage_settings_form = ManageSettingsForm(board= request.board, instance = request.board)
    if request.method == 'POST':
        manage_settings_form = ManageSettingsForm(board= request.board, instance = request.board, data = request.POST)
        if manage_settings_form.is_valid():
            manage_settings_form.save()
            return HttpResponseRedirect('.')
    payload = {'manage_settings_form':manage_settings_form}
    return render_to_response('management/index.html', payload, RequestContext(request))

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
@login_required
def upgrade(request):
    board = request.board
    if not request.user == request.board.owner:
        return HttpResponseForbidden('You do not have access to this board')
    pp = paypal.PayPal()
    cost = settings.UPGRADE_COST
    token = pp.SetExpressCheckout(cost, '%s%s'%(board.get_absolute_url(), reverse('manage_board_paypal_appr')), '%s%s'%(board.get_absolute_url(), reverse('manage_upgrade')), L_BILLINGTYPE0 = 'RecurringPayments', L_BILLINGAGREEMENTDESCRIPTION0 = 'Zobpress Upgrade')
    board_pp, created = BoardPayPal.objects.get_or_create(board = board)
    board_pp.paypal_token_sec = token
    board_pp.save()
    paypal_url = pp.PAYPAL_URL + token
    payload = {'paypal_url':paypal_url}
    return render_to_response('management/upgrade.html', payload, RequestContext(request))

@ensure_has_board
@login_required
def upgrade_approved(request):
    import pdb
    pdb.set_trace()
    board = request.board
    if not request.user == request.board.owner:
        return HttpResponseForbidden('You do not have access to this board')
    pp = paypal.PayPal()
    board_pp = BoardPayPal.objects.get(board = board)
    paypal_details = pp.GetExpressCheckoutDetails(board_pp.paypal_token_sec, return_all = True)
    cost = settings.UPGRADE_COST
    payload = {}
    if 'Success' in paypal_details['ACK']:
        payload['ack'] = True
        token = paypal_details['TOKEN'][0]
        payer_id = request.GET['PayerID']
        board_pp.paypal_token_gec = token
        board_pp.payer_id = payer_id
        board_pp.save()
        first_name = paypal_details['FIRSTNAME'][0]
        last_name = paypal_details['LASTNAME'][0]
        amt = paypal_details['AMT'][0]
        payload_update  = {'first_name':first_name, 'last_name':last_name, 'amt':amt}
        payload.update(payload_update)
        payment_details  = pp.DoExpressCheckoutPayment(token = token, payer_id = payer_id, amt = cost)
        if 'Success' in payment_details['ACK']:
            profile = request.user.get_profile()
            profile.is_paid = True
            profile.save()
            
        else:
            payload['ack'] = False
    else:
        payload['ack'] = False
    return render_to_response('management/upgrade_approved.html', payload, RequestContext(request))

    
    

