from zobpress.models import Board, Category

def populate_board(request):
    "Populate the board in the template"
    board = request.board
    if board:
        categories = Category.objects.filter(board = board)
    else:
        categories = []
    return {'board':request.board, 'categories':categories}
