from django.conf.urls import patterns, url
from boards.views import BoardPostList

urlpatterns = patterns(
    '',
    url(r'^boards/([0-9]+)/page/([0-9]+)?/$', 'boards.views.boardpage',
        name="boardpage"),
    url(r'^board/(?P<pk>[0-9]+)/page/$', BoardPostList.as_view(),
        name="board_post_list"),
    url(r'^board/(?P<pk>[0-9]+)/page/(?P<page>[0-9]+)/$', BoardPostList.as_view(),
        name="board_post_list"),
    url(r'^boards/([0-9]+)/post/([0-9]+)/$', 'boards.views.postpage',
        name="postpage"),
    url(r'^boards/([0-9]+)/post/$', 'boards.views.write', name="write"),
    url(r'^boards/([0-9]+)/search/$', 'boards.views.boardpage', name="search"),
    url(r'^boards/([0-9]+)/post/([0-9]+)/rewrite/', 'boards.views.rewrite',
        name="rewrite"),
    url(r'^boards/([0-9]+)/post/([0-9]+)/comment/([0-9]+)/delete/$',
        'boards.views.deletecomment', name="deletecomment"),
    url(r'^boards/([0-9]+)/post/([0-9]+)/$', 'boards.views.postpage',
        name="postpage"),
    url(r'^boards/([0-9]+)/post/([0-9]+)/delete/$', 'boards.views.deletepost', name="deletepost"),
    url(r'^boards/([0-9]+)/file-upload$', 'boards.cgis.file_upload', name="file_upload"),
    url(r'^boards/@([a-z0-9]*)$', 'boards.cgis.file_download', name="file_download"),
)
