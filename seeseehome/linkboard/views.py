from django.shortcuts import render
from django.http import HttpResponseRedirect
from seeseehome import msg
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from linkboard.models import LinkPost
from django.core.validators import URLValidator
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

    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(LinkBoard, self).get_context_data(**kwargs)

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

        for post in context['posts']:
            post.check_link_thumbnail() # check thumbnails
        
        context['mixed_posts'] = zip(context['posts'], indices)

        return context


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
