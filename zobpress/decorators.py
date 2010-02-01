from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.conf import settings

class ensure_has_board(object):
    "A decorator which ensures that a the url accessed has a corresponding board populated."
    def __init__(self, func):
        self.func = func
        
    def __call__(self, request, *args, **kwargs):
        if request.board:
            return self.func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('sitewide_register_board'))
        
def ensure_is_admin(view_func):
    "A decorator which ensures that only the Board Admin, or a superuser can access the board backend."
    def dec_func(request, *args, **kwargs):
        if can_access_board_backend(request.user, request.board):
            return view_func(*args, **kwargs)
        else:
            raise Http404
        
        
                
def can_access_board_backend(user, board):
    "Whether the given user can acess the given board backend."
    if board.owner == user:
        return True
    elif user.is_superuser:
        return True
    return False
    
            