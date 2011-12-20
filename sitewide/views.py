from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings

from sitewide.forms import NewBoardForms, ContactUsForm
from registration.views import register
from zobpress.models import Board

def index(request):
    from zobpress.models import Job
    try:
        latestjob = Job.objects.filter(is_default = False).latest()
    except Job.DoesNotExist:
        latestjob = None
    payload = {"latestjob": latestjob}
    return render_to_response('sitewide/index.html', payload, RequestContext(request))

def contact(request):
    form = ContactUsForm()
    if request.method == "POST":
        form = ContactUsForm(data = request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect(reverse("sitewide_contact_done"))
    payload = {"form": form}
    return render_to_response('sitewide/contact.html', payload, RequestContext(request))
    
def register_board(request):
     
    subdomain = getattr(request, "subdomain", None)
    if subdomain:
        new_board_form =  NewBoardForms(subdomain = subdomain)
    else:
        new_board_form =  NewBoardForms()
    if request.method == 'POST':
        new_board_form = NewBoardForms(data = request.POST)
        if new_board_form.is_valid():
            board, username, password = new_board_form.save()
            #Ok board is registered.
            #Login the new user and redirect them to their new board.
            request.session["board"] = board
            return HttpResponseRedirect(reverse("sitewide_register_board_done"))
            
    payload = {'new_board_form':new_board_form}
    return render_to_response('sitewide/register.html', payload, RequestContext(request))
    
    
def register_board_done(request, template):
    try:
        board = request.session["board"]
        del request.session["board"]
    except KeyError:
        board = None
    
    payload = {"board": board}
    return render_to_response(template, payload, RequestContext(request))
    

@login_required
def redirect_to_board(request):
    user_boards = Board.objects.filter(owner=request.user)
    if user_boards.count():
        board = user_boards[0]
        redirect_to = board.get_management_url()
        return HttpResponseRedirect(redirect_to)
        
    
def landingpage(request):
    new_board_form =  NewBoardForms()
    return render_to_response('sitewide/landingpage.html',
                              {'new_board_form':new_board_form},
                              RequestContext(request))
