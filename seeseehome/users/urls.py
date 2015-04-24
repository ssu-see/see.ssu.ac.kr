from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^sign-up/', 'users.views.signup', name="signup"),
    url(r'^sign-in/', 'users.views.signin', name="signin"),
    url(r'^logout/', 'users.views.logout', name="logout"),
    url(r'^mypage/$', 'users.views.personalinfo', name="mypage"),
    url(r'^mypage/editpersonalinfo/', 'users.views.editpersonalinfo',
        name="editpersonalinfo"),
    url(r'^mypage/editpwd/', 'users.views.editpassword',
        name="editpwd"),
)
