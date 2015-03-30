from boards.models import Board


def board_list(request):
    """
    render Google Analytics tracking ID ( UA-********-* ) to template
    """
    boardlist = Board.objects.all()

    return {
        'boardlist': boardlist
    }
