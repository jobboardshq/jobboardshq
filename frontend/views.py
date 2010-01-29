from django.shortcuts import render_to_response
from django.template.context import RequestContext


def index(request):
    board = request.board
    category = board.category_set.all()
    pages = board.page_set.all()
    jobs = board.job_set.all()
    return render_to_response("frontend/index.html", {"category":category, "pages": pages, "jobs": jobs}, RequestContext(request))

def addjob(request):
    return render_to_response("frontend/addjob.html", {}, RequestContext(request))

def subscribe(request):
    return render_to_response("frontend/subscribe.html", {}, RequestContext(request))

def apply(request, job_slug):
    pass
