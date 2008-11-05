from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

from management.forms import ManageSettingsForm
from zobpress.decorators import ensure_has_board

@ensure_has_board
def index(request):
    manage_settings_form = ManageSettingsForm(instance = request.board)
    if request.method == 'POST':
        manage_settings_form = ManageSettingsForm(instance = request.board, data = request.POST)
        if manage_settings_form.is_valid():
            manage_settings_form.save()
            return HttpResponseRedirect('.')
    payload = {'manage_settings_form':manage_settings_form}
    return render_to_response('management/index.html', payload, RequestContext(request))
