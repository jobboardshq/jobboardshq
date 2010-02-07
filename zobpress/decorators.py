from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.http import urlquote
from django.utils.functional import wraps
from django.utils.decorators import auto_adapt_to_methods
from django.contrib.auth import REDIRECT_FIELD_NAME

class ensure_has_board(object):
    "A decorator which ensures that a the url accessed has a corresponding board populated."
    def __init__(self, func):
        self.func = func
        
    def __call__(self, request, *args, **kwargs):
        if request.board:
            return self.func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('sitewide_register_board'))
        
def request_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Like django's user_passes_test, but the test function takes a request.
    """
    if not login_url:
        login_url = settings.LOGIN_URL

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            path = urlquote(request.get_full_path())
            tup = login_url, redirect_field_name, path
            return HttpResponseRedirect('%s?%s=%s' % tup)
        return _wrapped_view
    return decorator
        
        
    
def can_access_board_backend(request):
    "Whether the given user can access the given board backend."
    user, board = request.user, request.board
    if board.owner == user:
        return True
    elif user.is_superuser:
        return True
    return False
    
ensure_is_admin = request_passes_test(test_func = can_access_board_backend)            