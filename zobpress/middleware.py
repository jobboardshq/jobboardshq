from django.contrib.sites.models import Site
from django.conf import settings

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
            
