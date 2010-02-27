from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import feedgenerator

from emailsubs.forms import EmailCaptureForm
from emailsubs.models import EmailSubscription



def index(request):
    email_form = EmailCaptureForm(board = request.board)
    if request.method == "POST":
        print request.POST
        email_form = EmailCaptureForm(board = request.board, data = request.POST)
        if email_form.is_valid():
            email_form.save()
            return HttpResponseRedirect(reverse('emailsubs_index_done'))
    payload = {'email_form':email_form}
    return render_to_response('emailsubs/index.html', payload, RequestContext(request))

def confirm(request, id):
    email_sub = get_object_or_404(EmailSubscription, id = id)
    key = request.GET.get('key', '')
    if key == email_sub.key:
        confirm = True
        email_sub.is_confirmed = True
        email_sub.save()
    else:
        confirm = False
    payload = {'confirm':confirm, 'board':request.board}
    return render_to_response('emailsubs/confirm.html', payload, RequestContext(request))

def unsubscribe(request, id):
    email_sub = get_object_or_404(EmailSubscription, id = id)
    key = request.GET.get('key', '')
    if key == email_sub.key:
        valid = True
        email_sub.delete()
    else:
        valid = False
    payload = {'valid':valid}
    return render_to_response('emailsubs/unsubscribe.html', payload, RequestContext(request))
