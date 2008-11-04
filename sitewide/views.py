from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

from emailsubs.models import EmailSent
from sitewide.forms import NewBoardForms

def index(request):
    payload = {}
    return render_to_response('sitewide/index.html', payload, RequestContext(request))

def register_board(request):
    new_board_form = NewBoardForms()
    if request.method == 'POST':
        new_board_form = NewBoardForms(data = request.POST)
        if new_board_form.is_valid():
            new_board_form.save()
            
    payload = {'new_board_form':new_board_form}
    return render_to_response('sitewide/register.html', payload, RequestContext(request))
    
