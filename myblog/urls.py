from django.conf.urls import patterns, include, url
#from home.views import index
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', index, name='home_index'),
    # url(r'^myblog/', include('myblog.foo.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^comment/', include('comment.urls')),
    url(r'^photos/', include('photos.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
