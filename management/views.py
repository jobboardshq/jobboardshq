from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

from StringIO import StringIO

from management.forms import ManageSettingsForm
from zobpress.decorators import ensure_has_board
from zobpress.models import type_mapping, JobFormModel, JobFieldModel, Job, BoardPayments
from zobpress.models import EmployeeFormModel, EmployeeFieldModel, Category, Employee

@ensure_has_board
@login_required
def index(request):
    if not request.user == request.board.owner:
        return HttpResponseForbidden('You do not have access to this board')
    manage_settings_form = ManageSettingsForm(instance = request.board)
    if request.method == 'POST':
        manage_settings_form = ManageSettingsForm(instance = request.board, data = request.POST)
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

