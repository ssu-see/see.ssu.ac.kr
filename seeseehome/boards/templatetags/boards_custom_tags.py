from django import template
from boards.models import *
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def num_of_comments_in_post(post):
#    post = Post.objects.get_post(post_id)
    num_of_comments_in_post = Comment.objects.filter(post=post).count()
    return num_of_comments_in_post

@register.filter
def posts_last_2_weeks(board):
    posts = Post.objects.filter(board=board).order_by('-date_posted')
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=2)
    posts_last_2_weeks = posts.filter(
                             date_posted__range = (start_date, end_date)
                            )
    return posts_last_2_weeks.count()

@register.filter
def posts_last_3_days(board):
    posts = Post.objects.filter(board=board).order_by('-date_posted')
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3)
    posts_last_3_days = posts.filter(
                             date_posted__range = (start_date, end_date)
                            )
    return posts_last_3_days.count()

@register.filter
def slice_without_ext(string, count):
    splited = string.rsplit('.', 1)
    file_name = splited[0]
    ext = splited[1]

    return file_name[:count] + '....' + ext