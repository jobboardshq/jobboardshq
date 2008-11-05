from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

class ensure_has_board(object):
    def __init__(self, func):
        self.func = func
        
    def __call__(self, request, *args, **kwargs):
        if request.board:
            return self.func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('sitewide_register_board'))
            