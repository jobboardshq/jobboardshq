from zobpress.models import Board, Category
from django.conf import settings

def populate_board(request):
    "Populate the board in the template"
    board = request.board
    if board:
        categories = Category.objects.filter(board = board)
    else:
        categories = []
    return {'board':request.board, 'categories':categories, 'current_url': request.META['PATH_INFO'], "base_domain": settings.BASE_DOMAIN}

    
