from django.shortcuts import render_to_response
from django.template import RequestContext
from sitewide.forms import NewBoardForms, ContactUsForm

from registration.views import register
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login
from django.contrib.auth import authenticate

def index(request):
    payload = {}
    return render_to_response('sitewide/index.html', payload, RequestContext(request))

def contact(request):
    form = ContactUsForm()
    if request.method == "POST":
        form = ContactUsForm(data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("sitewide_contact_done"))
    payload = {"form": form}
    return render_to_response('sitewide/contact.html', payload, RequestContext(request))

def register_board(request):
    "This wrapper around the register view"
    #return register(request, form_class = NewBoardForms)
    new_board_form =  NewBoardForms(subdomain = request.subdomain)
    if request.method == 'POST':
        new_board_form = NewBoardForms(data = request.POST)
        if new_board_form.is_valid():
            board, username, password = new_board_form.save()
            #Ok board is registered.
            #Login the new user and redirect them to their new board.
            user = authenticate(username =username, password=password)
            login(request, user)
            user.message_set.create(message = "Your board has been created.")
            return HttpResponseRedirect(board.get_management_url())
            
    payload = {'new_board_form':new_board_form}
    return render_to_response('sitewide/register.html', payload, RequestContext(request))
    
    
