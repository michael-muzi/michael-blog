from django.conf.urls import patterns, include, url

urlpatterns = patterns('home.views',
    url(r'^$', 'index', name='home_index'),

)
