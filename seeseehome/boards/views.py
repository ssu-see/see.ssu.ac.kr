from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from boards.models import Board, AttachmentFile, Post, Comment
from users.models import User
from seeseehome import msg
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from ckeditor_form import CkEditorForm

from django.views.generic.list import ListView

from boards.utils.permission_handling import check_readperm_with_message


@login_required
def write(request, board_id, **extra_fields):
    board = Board.objects.get_board(board_id)
    writer = User.objects.get_user(request.user.id)

    if not Post.objects.is_valid_writeperm(
            board=board, writer=writer):
        messages.error(request, msg.boards_write_error)
        messages.info(request, msg.boards_writer_perm_error)
        return HttpResponseRedirect(reverse("boards:board_post_list",
                                            args=(board_id, 1)))

    if request.method == 'POST':
        is_valid_content = False
        is_notice = False

        subject = request.POST['subject']

        try:
            Post.objects.validate_subject(subject)
        except ValueError:
            messages.error(request, msg.boards_write_error)
            messages.info(request, msg.boards_post_subject_must_be_set)
            return HttpResponseRedirect(reverse("boards:write",
                                                args=(board_id)))
        except ValidationError:
            messages.error(request, msg.boards_write_error)
            messages.info(request, msg.boards_post_subject_at_most_255)
            return HttpResponseRedirect(reverse("boards:write",
                                                args=(board_id)))

        if 'content' in request.POST:
            content = request.POST['content']
            try:
                Post.objects.validate_content(content)
            except ValidationError:
                messages.error(request, msg.boards_write_error)
                messages.info(request, msg.boards_post_content_at_most_65535)
                return HttpResponseRedirect(reverse("boards:write",
                                                    args=(board_id)))
            else:
                is_valid_content = True

        if 'is_notice' in request.POST:
            is_notice = request.POST['is_notice']

        if 'post_id' not in extra_fields:
            post = Post.objects.create_post(board=board, subject=subject,
                                            writer=writer, is_notice=is_notice)

            if is_valid_content:
                Post.objects.update_post(post.id, content=content)

            if 'file_keys' in request.POST:
                for file_key in request.POST.getlist('file_keys'):
                    attachment_file = AttachmentFile.objects.file_by_hash_key(file_key)
                    if attachment_file is not None:
                        Post.objects.update_post(post.id, attachment_file=attachment_file)

            return HttpResponseRedirect(reverse("boards:postpage",
                                                args=(board_id, post.id)))

        # If rewrite, no create, but update
        else:
            post_id = extra_fields['post_id']
            Post.objects.update_post(post_id, subject=subject)

            if is_valid_content:
                Post.objects.update_post(post_id, content=content,
                                         is_notice=is_notice)

            if 'file_keys' in request.POST:
                for file_key in request.POST['file_keys']:
                    attachment_file = AttachmentFile.objects.file_by_hash_key(file_key)
                    if attachment_file is not None:
                        Post.objects.update_post(post_id, attachment_file=attachment_file)

            messages.success(request, msg.boards_write_success)
            messages.info(request, msg.boards_write_success_info)

    ck_editor_form = CkEditorForm()

    return render(request,
                  "boards/write.html",
                  {'board': board,
                   'ckeditor_form': ck_editor_form})


@login_required
def rewrite(request, board_id, post_id):
    board = Board.objects.get_board(board_id)
    post = Post.objects.get_post(post_id)

    if request.method == 'POST':
        write(request, board_id, post_id=post_id)
        return HttpResponseRedirect(reverse("boards:postpage",
                                            args=(board_id, post_id)))

    ck_editor_form = CkEditorForm({'content': post.content})

    return render(request, "boards/write.html",
                  {'board': board, 'post': post, 'ckeditor_form': ck_editor_form})


def postpage(request, board_id, post_id):
    board = Board.objects.get_board(board_id)
    post = Post.objects.get_post(post_id)

    if not post.board == board:
        raise Http404

    reader = User.objects.get_user(request.user.id)
    if check_readperm_with_message(request, board_id) is False:
        return HttpResponseRedirect(reverse("home"))

    if reader is None:
        Post.objects.hit_count(post.id)
    elif post.writer.id is not reader.id:
        Post.objects.hit_count(post.id)

    if request.method == "POST":
        comment = request.POST['comment']
        try:
            Comment.objects.validate_comment(comment)
        except ValueError:
            messages.error(request, msg.board_comment_error)
            messages.info(request, msg.board_comment_must_be_set)
        except ValidationError:
            messages.error(request, msg.board_comment_error)
            messages.info(request, msg.board_comment_at_most_255)
        else:

            try:
                Comment.objects.create_comment(
                    writer=request.user, board=board,
                    post=post, comment=comment
                )
            except ValidationError:
                messages.error(request, "Comment permission error")

    commentlist = Comment.objects.filter(post=post)

    return render(request, "boards/postpage.html",
                  {
                      'board': board, 'post': post, 'commentlist': commentlist,
                      'attachments_count': post.attachments.count(),
                  })


def pagination(posts, posts_per_page=10, page_num=1):
    #   posts per page
    start_pos = (page_num - 1) * posts_per_page
    end_pos = start_pos + posts_per_page
    posts_of_present_page = posts[start_pos: end_pos]

    paginator = Paginator(posts, posts_per_page)
    p = paginator.page(page_num)

    has_next = p.has_next()
    has_previous = p.has_previous()

    if has_next:
        next_page_num = p.next_page_number()
    else:
        next_page_num = page_num

    if has_previous:
        previous_page_num = p.previous_page_number()
    else:
        previous_page_num = page_num

    next_10_page_num = page_num + 10 if page_num + 10 < paginator.num_pages else paginator.num_pages
    previous_10_page_num = page_num - 10 if page_num - 10 > 1 else 1

    page_range = paginator.page_range

    if page_num % 10 == 0:
        page_range = paginator.page_range[(int(page_num / 10) - 1) * 10: (int(page_num / 10) - 1) * 10 + 10]
    else:
        page_range = paginator.page_range[int(page_num / 10) * 10: int(page_num / 10) * 10 + 10]

    custom_paginator = {
        'posts': posts_of_present_page,
        'paginator': p,
        'page_range': page_range,
        'has_next': has_next,
        'has_next_10': paginator.num_pages >= page_num + 10,
        'has_previous': has_previous,
        'has_previous_10': 0 < page_num - 10,
        'next_10_page_num': next_10_page_num,
        'next_page_num': next_page_num,
        'previous_10_page_num': previous_10_page_num,
        'previous_page_num': previous_page_num,
    }
    return custom_paginator


class BoardPostList(ListView):
    template_name = "boards/board.html"

    model = Post
    context_object_name = 'posts'

    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if check_readperm_with_message(request, self.kwargs['pk']) is False:
            return HttpResponseRedirect(reverse("home"))

        return super(BoardPostList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        queryset = super(BoardPostList, self).get_queryset(**kwargs)
        return queryset.filter(board=Board.objects.get(pk=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        context = super(BoardPostList, self).get_context_data(**kwargs)

        context['board'] = Board.objects.get(pk=self.kwargs['pk'])

        context['current_page'] = context['page_obj'].number
        last_page = context['page_obj'].paginator.num_pages
        context['start_page'] = context['current_page'] % 10 == 0 and \
            (context['current_page'] / 10 - 1) * 10 + 1 or \
            context['current_page'] / 10 * 10 + 1
        context['end_page'] = last_page > context['start_page'] + 9 and \
            context['start_page'] + 9 or last_page
        context['page_range'] = range(
            context['start_page'], context['end_page'] + 1
        )

        context['next_page'] = last_page > context['end_page'] and \
            context['end_page'] + 1 or 0
        context['prev_page'] = context['start_page'] - 10 > 0 and \
            context['start_page'] - 1 or 0

        last_index = context['page_obj'].paginator.count
        start_index = context['page_obj'].start_index()
        end_index = context['page_obj'].end_index()
        indices = list(reversed(range(
            last_index - end_index + 1, last_index - start_index + 2))
        )
        context['mixed_posts'] = zip(context['posts'], indices)

        return context


@login_required
def deletecomment(request, board_id, post_id, comment_id):
    comment = Comment.objects.get_comment(comment_id)
    if request.user != comment.writer:
        messages.error(request, msg.boards_delete_comment_error)
        messages.info(request, msg.boards_delete_comment_auth_error)
    else:
        comment.delete()

    return HttpResponseRedirect(reverse("boards:postpage",
                                        args=(board_id, post_id)))


@login_required
def deletepost(request, board_id, post_id):
    post = Post.objects.get_post(post_id)

    if request.user != post.writer:
        messages.error(request, msg.boards_delete_post_error)
        messages.info(request, msg.boards_delete_post_auth_error)
    else:
        post.delete()

    return HttpResponseRedirect(reverse("boards:board_post_list",
                                        args=(board_id, 1)))
