from zobpress.models import Board

def populate_board(request):
    "Populate the board in the template"
    return {'board':request.board}