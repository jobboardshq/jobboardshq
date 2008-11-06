from zobpress.models import Board

import urlparse

class GetSubdomainMiddleware:
    
    def process_request(self, request):
        import logging
        logging.debug(request.META['HTTP_HOST'])
        bits = urlparse.urlsplit(request.META['HTTP_HOST'])[0].split('.')
        if not( len(bits) == 3):
            pass#Todo Raise an exception etc
            bits = urlparse.urlsplit(request.META['HTTP_HOST'])[3].split('.')
            if not( len(bits) == 3):
                bits = request.META['HTTP_HOST'].split('.')
                if not( len(bits) == 3):
                    pass
                    #raise Exception("There was a problem getting the subdomain")
        request.subdomain = bits[0]
        try:
            board = Board.objects.get(subdomain = request.subdomain)
            request.board = board
        except Board.DoesNotExist:
            request.board = None
        return None
