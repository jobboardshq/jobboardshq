
from django.conf import settings

from zobpress.decorators import can_access_board_backend
from zobpress.models import Board, Category

def populate_board(request):
    "Populate the board in the template"
    board = request.board
    if board:
        categories = Category.objects.filter(board = board)
        board_settings = board.settings
    else:
        categories = []
        board_settings = None
    return {'board':request.board, 'categories':categories, "board_settings": board_settings, 'current_url': request.META['PATH_INFO'], "base_domain": settings.BASE_DOMAIN, 'debug': settings.DEBUG, 'is_board_admin': can_access_board_backend(request)}

    
