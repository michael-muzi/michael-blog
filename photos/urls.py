from django.conf.urls import patterns, include, url

urlpatterns = patterns('photos.views',
    url(r'^upload/$', 'upload_image', name='upload_image'),
)
