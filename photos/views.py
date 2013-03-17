from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from photos.models import PhotoItem, PhotoAlbum
from photos.froms import PhotoForm

@login_required
def upload_image(request, mimetype=None):
    username = request.POST.get('username',request.user.username)
    user = User.objects.get(username=username)
    album_id = request.POST.get('album_id',None)
    if request.method=='POST':
        photo_url = request.POST.get('photo_url', None)
        photo_form = PhotoForm(user, request.POST, request.FILES)
        if photo_form.is_valid():
            photo = PhotoItem()
            photo.image = photo_form.cleaned_data['image']
            photo.descr = photo_form.cleaned_data['descr']
            photo.save()
            
            if album_id:
                album = PhotoAlbum.objects.get(id=int(album_id))
            else:
                name = 'DefaultAlbum'
                if photo_form.cleaned_data.get('new_album',None):
                    name = photo_form.cleaned_data['new_album']
                    
                album, created = PhotoAlbum.objects.get_or_create(author=user, name=name, defaults={'cover': photo})
                          
            photo.album = album
            photo.save()
            data = {"image_url":photo.image.thumb_url, "id":photo.id, 'album_id':photo.album.id}
            
            return HttpResponse(simplejson.dumps(data,ensure_ascii = False))
        else:
            return HttpResponse(simplejson.dumps(photo_form,ensure_ascii = False))
        return HttpResponseBadRequest(0)

