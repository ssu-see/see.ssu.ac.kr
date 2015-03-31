from boards.models import Board
from seeseehome import msg
from django.contrib import messages


def _is_valid_readperm(board, user):
    return user.userperm in board.readperm


def check_readperm_with_message(request, board_pk):
    board = Board.objects.get(pk=board_pk)

    if request.user.is_anonymous() is True:
        if '0' not in board.readperm:
            messages.error(request, msg.boards_read_error)
            messages.info(request, msg.boards_read_error_info)
            return False
    elif not _is_valid_readperm(
            board=board, user=request.user):
        messages.error(request, msg.boards_read_error)
        messages.info(request, msg.boards_read_error_info)
        return False

    return True
