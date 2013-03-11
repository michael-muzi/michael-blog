from django.conf.urls import patterns, include, url

urlpatterns = patterns('users.views',
    url(r'^sign-up/$', 'register', name='register_user'),
    url(r'^login/$', 'login_view', name='login_view'),
    url(r'^logout/$', 'logout_view', name='user_logout'),
)
