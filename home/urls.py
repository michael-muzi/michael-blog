from django.conf.urls import patterns, include, url

urlpatterns = patterns('home.views',
    url(r'^$', 'index', name='home_index'),
    
    #essay editor
    url(r'^essay/$', 'essay', name='essay'),
    url(r'^essay/write/$', 'essay_write', name='essay_write'),
    url(r'^essay/delete/(?P<id>[0-9]+)/$', 'essay_rm', name='essay_delete'),
    
    url(r'^essay/detail/(?P<id>[0-9]+)/$', 'essay_detail', name='essay_detail'),
    
    #essay search
    url(r'^essay/search/$', 'search', name='essay_search'),
    url(r'^essay/search/tag/(?P<tag_id>[0-9]+)/$', 'search', name='search_tag'),
    url(r'^essay/search/type/(?P<type_id>[0-9]+)/$', 'search', name='search_type'),
    
)
