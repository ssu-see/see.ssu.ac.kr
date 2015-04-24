from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from seeseehome import msg
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from linkboard.models import LinkPost
from django.core.validators import URLValidator
from boards import views

from django.views.generic.list import ListView


@login_required
def linkpost(request, **extra_fields):
    writer = request.user

    if not LinkPost.objects.is_valid_writeperm_to_linkpost(writer=writer):
        messages.error(request, msg.boards_write_error)
        messages.info(request, msg.boards_writer_perm_error)
        return HttpResponseRedirect(
            reverse("linkboard:linkboard"))

    if request.method == 'POST':
        try:
            url = request.POST['url']
            urlvalidator = URLValidator()
            urlvalidator(url)
        except ValidationError:
            messages.error(request, msg.linkboard_linkpost_error)
            messages.info(request, msg.linkboard_linkpost_invalid)
            return HttpResponseRedirect(
                reverse("linkboard:linkboard"))

        except UnicodeError:
            messages.error(request, msg.linkboard_linkpost_error)
            messages.info(request, msg.linkboard_linkpost_unicode_error)
            return HttpResponseRedirect(
                reverse("linkboard:linkboard"))

        try:
            description = request.POST['description']
            LinkPost.objects.validate_description(description)
        except ValueError:
            messages.error(request, msg.linkboard_linkpost_error)
            messages.info(request, msg.boards_linkpost_description)
        except ValidationError:
            messages.error(request, msg.linkboard_linkpost_error)
            messages.info(
                request,
                msg.boards_linkpost_description_at_most_255
            )

        if 'post_id' not in extra_fields:
            #           create link post
            LinkPost.objects.create_linkpost(
                writer=writer,
                url=url,
                description=description
            )
            messages.success(request, msg.linkboard_linkpost_success)
            return HttpResponseRedirect(
                reverse("linkboard:linkboard"))

        else:
            post_id = extra_fields['post_id']
            LinkPost.objects.update_linkpost(linkpost_id=post_id,
                                             url=url, description=description)
            messages.success(request, msg.linkboard_linkpost_success)
            return HttpResponseRedirect(
                reverse("linkboard:linkboard"))

    return render(request, "linkboard/linkpost.html")


class LinkBoard(ListView):
    template_name = "linkboard/linkboard.html"

    model = LinkPost
    context_object_name = 'posts'

    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(LinkBoard, self).get_context_data(**kwargs)

        context['current_page'] = context['page_obj'].number
        print context['page_obj']
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
def linkboard(request, page=1):
    posts = LinkPost.objects.all().order_by('-date_posted')
    posts_per_page = 10

    try:
        page = int(page)
    except:
        raise Http404

    if request.method == "POST":
        search_decription = request.POST['search_description']
        posts = posts.filter(description__icontains=search_decription)
        posts = posts[0:50]
        return render(request, "linkboard/linkboard.html",
                      {
                          'posts': posts,
                          'searchvalue': search_decription,
                          'top50': "Top 50 Search",
                      }
                      )

#   if the page does not exist, raise 404
    try:
        custom_paginator = views.pagination(
            posts=posts,
            posts_per_page=10,
            page_num=page
        )
    except:
        raise Http404

    return render(request, "linkboard/linkboard.html",
                  {
                      'post_base_index': (posts_per_page * (page - 1)),
                      'posts': custom_paginator['posts'],
                      'paginator': custom_paginator['paginator'],
                      'has_next': custom_paginator['has_next'],
                      'has_next_10': custom_paginator['has_next_10'],
                      'current_page_num': page,
                      'has_previous': custom_paginator['has_previous'],
                      'has_previous_10': custom_paginator['has_previous_10'],
                      'page_range': custom_paginator['page_range'],
                      'next_page_num': custom_paginator['next_page_num'],
                      'previous_page_num': custom_paginator['previous_page_num'],
                      'next_10_page_num': custom_paginator['next_10_page_num'],
                      'previous_10_page_num': custom_paginator['previous_10_page_num'],
                  })


@login_required
def updatelinkpost(request, post_id):
    post = LinkPost.objects.get_linkpost(post_id)
    if request.method == 'POST':
        linkpost(request, post_id=post_id)
        return HttpResponseRedirect(reverse("linkboard:linkboard"))

    return render(request, "linkboard/updatelinkpost.html",
                  {'post': post})


@login_required
def deletelinkpost(request, post_id):
    linkpost = LinkPost.objects.get_linkpost(post_id)
#    print linkpost.writer
    if request.user != linkpost.writer:
        messages.error(request, msg.boards_delete_post_error)
        messages.info(request, msg.boards_delete_post_auth_error)
    else:
        linkpost.delete()

    return HttpResponseRedirect(reverse("linkboard:linkboard"))
