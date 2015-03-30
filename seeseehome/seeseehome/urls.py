from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
# Caution : Never upload sercurity_information file anywhere
try:
    from seeseehome import security_information
    ADMIN_URL = security_information.ADMIN_URL
except:
    ADMIN_URL = "admin_for_insecure_because_not_set_secret_admin_url"

urlpatterns = patterns(
    '',
    # admin page
    url(r'^' + ADMIN_URL + '/', include(admin.site.urls), name="admin"),

    # main page
    url(r'^$', 'seeseehome.views.home', name='home'),

    # about us
    url(r'^aboutus/', 'seeseehome.views.aboutus', name='aboutus'),

    # Django Apps
    url(r'^', include('users.urls', namespace='users')),
    url(r'^', include('boards.urls', namespace='boards')),
    url(r'^', include('linkboard.urls', namespace='linkboard')),

    #   Django third party modules
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
)

if settings.MEDIA_ENABLED:
    urlpatterns += patterns("",
                            (r'^media/(?P<path>.*)$',
                             'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}))
