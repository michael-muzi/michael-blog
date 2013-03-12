from django.conf.urls import patterns, include, url

urlpatterns = patterns('comment.views',
    url(r'^essay/$', 'comment_view', name='comment_essay'),
    
)
