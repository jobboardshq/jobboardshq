

def board_categories(request):
    if request.board:
        board = request.board
        category = board.category_set.all()
        pages = board.page_set.all()
        job_types = board.jobtype_set.filter(is_deleted=False)
        return {'pages':pages,
                'category':category,
                'job_types':job_types,
                }
    return {}
    