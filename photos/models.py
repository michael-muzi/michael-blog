# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from photos.image_field import ThumbnailImageField, ThumbnailImageFieldFile
from myblinapp.util.comentandflag import FlagManager
#import urllib

class PhotoAlbum(models.Model):
    name = models.CharField(blank=True, max_length=128, verbose_name=_("album name"))
    descr = models.TextField(blank=True, verbose_name=_("album description"))
    cover = models.ForeignKey('photos.PhotoItem',blank=True, null=True, related_name=u"title_photo")
    author = models.ForeignKey(User, verbose_name=_("author"))
    date_create = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("create time"))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-id']

    @models.permalink
    def get_absolute_url(self):
        return('album_detail', (), {'username': self.author.username, 'album_id': self.pk })

class PhotoItem(models.Model):
    descr = models.CharField(blank=True, max_length=128, verbose_name=_("album description"))
    image = ThumbnailImageField(upload_to='photos/%Y/%b/%d', blank=False, verbose_name=_("image url"))
    album = models.ForeignKey(PhotoAlbum, blank=True, null=True, verbose_name=_(" foreignkey album "))
    date_create = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("create time"))
  
    def __unicode__(self):
        return self.image.thumb_url

    class Meta:
        ordering = ['-id']

    @models.permalink
    def get_absolute_url(self):
        return('photo_detail', (), {'username': self.album.author.username, 'album_id': self.album.pk, 'photo_id': self.pk })
