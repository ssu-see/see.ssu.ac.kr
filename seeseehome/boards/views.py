from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request, Http404
from boards.models import *
from seeseehome import msg
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from boards.forms import WriteForm
from django.core.paginator import Paginator
from ckeditor_form import CkEditorForm

def check_invalid_readperm_with_message(request, board, reader):
#   Does the writer has valid write permission?
    if reader is None:
        if '0' not in board.readperm:
            messages.error(request, msg.boards_read_error)
            messages.info(request, msg.boards_read_error_info)
            return False
    elif not Board.objects.is_valid_readperm(
           board = board, reader = reader):
        messages.error(request, msg.boards_read_error)
        messages.info(request, msg.boards_read_error_info)
        return False 
    
    return True

@login_required
def write(request, board_id, **extra_fields):
#   django-ckform not used. 
#   ckeditor widget class is used in template instead)
#   form = WriteForm()

#   for prevent the error "referenced before assignment"
    #post_id = None

#   board : argument for is_valid_writeperm
    board = Board.objects.get_board(board_id)

#   writer : argument for is_valid_writeperm
    writer = User.objects.get_user(request.user.id)

#   does the writer have valid write permission?
    if not Post.objects.is_valid_writeperm(
           board = board, writer = writer):
        messages.error(request, msg.boards_write_error)
        messages.info(request, msg.boards_writer_perm_error)
        return HttpResponseRedirect(reverse("boards:boardpage", 
            args=(board_id, 1)))

    if request.method == 'POST':
        is_valid_content = False
        is_notice = False
#       subject
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

#       content
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

#       is_notice
        if 'is_notice' in request.POST:
            is_notice = request.POST['is_notice']

#       post save
        if not 'post_id' in extra_fields:
            post = Post.objects.create_post(board=board, subject=subject, 
                    writer=writer, is_notice=is_notice)
#           content save
            if is_valid_content:
                Post.objects.update_post(post.id, content=content)

            if 'file_keys' in request.POST:
                for file_key in request.POST.getlist('file_keys'):
                    attachment_file = AttachmentFile.objects.file_by_hash_key(file_key)
                    if not attachment_file == None:
                        Post.objects.update_post(post.id, attachment_file=attachment_file)

            return HttpResponseRedirect(reverse("boards:postpage",
                    args=(board_id, post.id)))
#       If rewrite, no create, but update
        else:
            post_id = extra_fields['post_id']
            Post.objects.update_post(post_id, subject=subject)

            if is_valid_content:
                Post.objects.update_post(post_id, content=content,
                    is_notice = is_notice)

            if 'file_keys' in request.POST:
                for file_key in request.POST['file_keys']:
                    attachment_file = AttachmentFile.objects.file_by_hash_key(file_key)
                    if not attachment_file == None:
                        Post.objects.update_post(post_id, attachment_file=attachment_file)

            messages.success(request, msg.boards_write_success)
            messages.info(request, msg.boards_write_success_info)
#           no need to HttpResponseRedirect, That is inplementeed in 
#           rewrite mothod

    boardlist = Board.objects.all()
    ck_editor_form = CkEditorForm()

    return render(request, "boards/write.html", {'boardlist' : boardlist, 'board' : board, 'ckeditor_form' : ck_editor_form})

@login_required
def rewrite(request, board_id, post_id):
    board = Board.objects.get_board(board_id)
#    boardposts = BoardPosts.objects.filter(board=board)
    post = Post.objects.get_post(post_id) 
    posts = Post.objects.filter(board=board)
    
    if request.method == 'POST':
        write(request, board_id, post_id=post_id)
        posts = Post.objects.filter(board=board).order_by("-date_posted")
        return HttpResponseRedirect(reverse("boards:postpage",
            args=(board_id, post_id)))

    boardlist = Board.objects.all()
    ck_editor_form = CkEditorForm({'content' : post.content})

    return render(request, "boards/write.html",
            {'board' : board, 'post' : post, 'boardlist' : boardlist, 'ckeditor_form' : ck_editor_form})

def postpage(request, board_id, post_id):
    board = Board.objects.get_board(board_id)
    post = Post.objects.get_post(post_id) 
    
    if not post.board == board:
        raise Http404

#   reader : for is_valid_readperm
    reader = User.objects.get_user(request.user.id)
    if check_invalid_readperm_with_message(request, board, reader) is False:
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
            Comment.objects.create_comment(
                writer=request.user, board = board,
                post = post, comment = comment
            )

    commentlist = \
        Comment.objects.filter(post=post).order_by('date_commented')

    boardlist = Board.objects.all()
    return render(request, "boards/postpage.html",
            {
                'board' : board, 'post' : post, 'boardlist' : boardlist,
                'commentlist' : commentlist, 'attachments_count' : post.attachments.count(),
            })

def pagination(posts, posts_per_page = 10, page_num = 1):
#   posts per page
    start_pos = (page_num - 1) * posts_per_page
    end_pos = start_pos + posts_per_page
    posts_of_present_page = posts[start_pos : end_pos]

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
                               'posts' : posts_of_present_page,
                               'paginator' : p,
                               'page_range' : page_range,
                               'has_next' : has_next,
                               'has_next_10' : paginator.num_pages >= page_num + 10,
                               'has_previous' : has_previous,
                               'has_previous_10' : 0 < page_num - 10,
                               'next_10_page_num' : next_10_page_num,
                               'next_page_num' : next_page_num,
                               'previous_10_page_num' : previous_10_page_num,
                               'previous_page_num' : previous_page_num,
                       }
    return custom_paginator

def boardpage(request, board_id, page=1):
#   board : for is_valid_readperm
    board = Board.objects.get_board(board_id)

#   reader : for is_valid_readperm
    reader = User.objects.get_user(request.user.id)
    posts_per_page = 10

    try:
        page = int(page)
    except:
        raise Http404

#   Does the reader has valid write permission?
    if check_invalid_readperm_with_message(request, board, reader) is False:
        return HttpResponseRedirect(reverse("home"))

#   The following line is important to the page list (prev page, next page)
    posts = Post.objects.filter(board=board).order_by("-date_posted")

#   Caution : Following lines are implemented after ordering post data
#   Is there a request method of post that searches specific posts?
    if request.method == "POST":
        search_post = request.POST['search_post']

        if request.POST['select_post'] == "subject":
            posts = posts.filter(subject__icontains = search_post)
        elif request.POST['select_post'] == "content":
            posts = posts.filter(content__icontains = search_post)
        elif request.POST['select_post'] == "subject + content":
            posts = posts.filter(subject__icontains = search_post) | \
                    posts.filter(content__icontains = search_post)
        elif request.POST['select_post'] == "writer":
            try:
                writer = User.objects.get(username = search_post)
            except ObjectDoesNotExist:
                messages.error(request, msg.boards_search_post_error)
                messages.info(request, msg.users_username_does_not_exist)
                return HttpResponseRedirect(reverse("boards:boardpage", 
                    args=(board.id, 1)))
            else:
                posts = posts.filter(writer = writer)
        
        posts = posts[0:50]
#       for board list of menu bar
        boardlist = Board.objects.all()    
        return render(request, "boards/boardpage.html",
                   {
                       'posts' : posts,
                       'board' : board,
                       'boardlist' : boardlist,
                       'searchvalue' : search_post,
                       'top50' : "Top 50 Search",
                   }
               )

    """
    All posts are listed in order by posted date.
    But First of all, notice post will be listed.
    """
    notices = posts.filter(is_notice = 1)
    posts = posts.filter(is_notice = 0)

#   if page does not exist, then raise 404
    try:    
        custom_paginator = pagination(posts=posts, posts_per_page = posts_per_page, page_num=page)
    except Exception as e:
        raise Http404

#   for board list of menu bar
    boardlist = Board.objects.all()
    return render(request, "boards/boardpage.html", 
               {
                   'board' : board,
                   'boardlist' : boardlist,
                   'notices' : notices,
                   'post_base_index': (posts_per_page * (page - 1)),
                   'posts' : custom_paginator['posts'],
                   'paginator' :custom_paginator['paginator'],
                   'has_next' : custom_paginator['has_next'],
                   'has_next_10' : custom_paginator['has_next_10'],
                   'current_page_num' : page,
                   'has_previous' : custom_paginator['has_previous'],
                   'has_previous_10' : custom_paginator['has_previous_10'],
                   'page_range' : custom_paginator['page_range'],
                   'next_page_num' : custom_paginator['next_page_num'],
                   'previous_page_num' : custom_paginator['previous_page_num'],
                   'next_10_page_num' : custom_paginator['next_10_page_num'],
                   'previous_10_page_num' : custom_paginator['previous_10_page_num'],
               }
           )

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
    
    return HttpResponseRedirect(reverse("boards:boardpage", 
      args=(board_id, 1)))
