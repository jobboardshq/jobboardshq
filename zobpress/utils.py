from zobpress.models import Board, Job, JobFormModel

def create_inital_form(board):
    """When a board is first registered, create the default board for them."""
    JobFormModel.objects.create_default_form(board)
