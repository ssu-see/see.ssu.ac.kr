from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^sign-up/', 'users.views.signup', name="signup"),
    url(r'^sign-in/', 'users.views.signin', name="signin"),
    url(r'^logout/', 'users.views.logout', name="logout"),
    url(r'^personalinfo/$', 'users.views.personalinfo', name="personalinfo"),
    url(r'^personalinfo/editpersonalinfo/', 'users.views.editpersonalinfo', 
      name="editpersonalinfo"),
    url(r'^personalinfo/editpwd/', 'users.views.editpassword', 
      name="editpwd"),
)

