from django.shortcuts import render_to_response
from django.template import RequestContext
from sitewide.forms import NewBoardForms, ContactUsForm

from registration.views import register

def index(request):
    payload = {}
    return render_to_response('sitewide/index.html', payload, RequestContext(request))

def contact(request):
    form = ContactUsForm()
    payload = {"form": form}
    return render_to_response('sitewide/contact.html', payload, RequestContext(request))

def register_board(request):
    "This wrapper around the register view"
    #return register(request, form_class = NewBoardForms)
    new_board_form =  NewBoardForms()
    if request.method == 'POST':
        new_board_form = NewBoardForms(data = request.POST)
        if new_board_form.is_valid():
            new_board_form.save()
            
    payload = {'new_board_form':new_board_form}
    return render_to_response('sitewide/register.html', payload, RequestContext(request))
    
    
