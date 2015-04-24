from django.conf.urls import patterns, include, url
from linkboard.views import LinkBoard


urlpatterns = patterns(
    '',
    url(r'^linkboard/$', LinkBoard.as_view(), name="linkboard"),
    url(r'^linkboard/([0-9]+)/$', LinkBoard.as_view(), name="linkboard"),
    url(r'^linkboard/linkpost/$', 'linkboard.views.linkpost', name="linkpost"),
    url(r'^linkboard/linkpost/([0-9]+)/delete/', 'linkboard.views.deletelinkpost', name="deletelinkpost"),
    url(r'^linkboard/linkpost/([0-9]+)/update/', 'linkboard.views.updatelinkpost', name="updatelinkpost"),
)
