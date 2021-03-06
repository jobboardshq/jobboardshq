
from django.contrib.sites.models import Site
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import urlparse

from zobpress.models import Board

class GetSubdomainMiddleware:
    
    def process_request(self, request):
        bits = urlparse.urlparse(request.build_absolute_uri()).hostname.split('.')
        if len(bits) > 2:
            request.subdomain = bits[0]
        else:
            request.subdomain = None
        probable_domain =  '.'.join(bits[1:])
        # print bits, request.subdomain, probable_domain, settings.BASE_DOMAIN
        # current_site = Site.objects.get_current()
        if settings.BASE_DOMAIN == probable_domain and request.subdomain:
            #User is using a subdomain.
            try:
                board = Board.objects.get(subdomain = request.subdomain)
                request.board = board
            except Board.DoesNotExist:
                request.board = None
        else:
            #User is using a Custom Domain
            try:
                domain = urlparse.urlsplit(request.build_absolute_uri()).hostname
                board = Board.objects.get(domain = domain)
                request.board = board
            except Board.DoesNotExist:
                request.board = None
                


class RedirectOnInvalidSubdomain(object):
    "This middleware *must be After* the GetSubdomainMiddleware, as it expects subdomain to be set up"
    def process_request(self, request):
        
        registration_path = reverse('sitewide_register_board')
        if not request.subdomain:
            #No subdomain is set, can't do anything special.
            return
        if request.subdomain in settings.UNALLOWED_SUBDOMAINS:
            return 
        if (not request.board) and  (not registration_path in request.path) and (not settings.MEDIA_URL in request.path) and (not '/admin/' in request.path):
            "We do not know what this subdomain is about. ask for registering"
            return HttpResponseRedirect(registration_path)

# threadlocals middleware
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()
def get_current_board():
    return getattr(_thread_locals, 'board', None)

class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        _thread_locals.board = getattr(request, 'board', None)

            
