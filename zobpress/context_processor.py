from zobpress.models import Board, Category

def populate_board(request):
    "Populate the board in the template"
    board = request.board
    categories = Category.objects.filter(board = board)
    return {'board':request.board, 'categories':categories}
