from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^linkboard/([0-9]+)/$', 'linkboard.views.linkboardpage',
                           name="linkboardpage"),
                       url(r'^linkboard/linkpost/$', 'linkboard.views.linkpost',
                           name="linkpost"),
                       url(r'^linkboard/linkpost/([0-9]+)/delete/',
                           'linkboard.views.deletelinkpost', name="deletelinkpost"),
                       url(r'^linkboard/linkpost/([0-9]+)/update/',
                           'linkboard.views.updatelinkpost', name="updatelinkpost"),
                       )
