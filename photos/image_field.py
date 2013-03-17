# -*- coding:utf-8 -*-
from django.db.models.fields.files import ImageField, ImageFieldFile
from django.conf import settings

try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps    
import os
from django.conf import settings
import hashlib
import time
import datetime
import random

def auto_crop(imgData, width=96, height=96):    
    imgSrcSize = imgData.size
    if width / height > imgSrcSize[0] / imgSrcSize[1]:
        newHeight = imgSrcSize[1] * width / imgSrcSize[0]
        imgData = imgData.resize((width, newHeight), Image.ANTIALIAS)
        imgData = imgData.transform((width, height), Image.EXTENT, (0, 0, width, height))
    else:
        newWidth = imgSrcSize[0] * height / imgSrcSize[1]
        offset = int((newWidth - width) / 2)
        imgData = imgData.resize((newWidth, height), Image.ANTIALIAS)
        imgData = imgData.transform((width, height), Image.EXTENT, (0 + offset, 0, width + offset, height))
    return imgData

class ThumbnailImageFieldFile(ImageFieldFile):
    def _add_postfix_dir(self, postfix, s):
        parts = s.split(".")
        s = "%s%s.%s.%s" % (settings.MEDIA_ROOT, parts[-2], postfix, parts[-1].lower())
        return s

    def _add_postfix_url(self, postfix, s):
        parts = s.split(".")
        s = "%s%s.%s.%s" % (settings.MEDIA_URL, parts[-2], postfix, parts[-1].lower())
        return s

    def _get_normal_path(self):
        return self._add_postfix_dir("normal", self.name)
    normal_path = property(_get_normal_path)

    def _get_normal_url(self):
        return self._add_postfix_url("normal", self.name)
    normal_url = property(_get_normal_url)

    def _get_thumb_path(self):
        return self._add_postfix_dir("thumb", self.name)
    thumb_path = property(_get_thumb_path)

    def _get_thumb_url(self):
        return self._add_postfix_url("thumb", self.name)
    thumb_url = property(_get_thumb_url)
    
    def _get_icon_path(self):
        return self._add_postfix_dir("icon", self.name)
    icon_path = property(_get_icon_path)

    def _get_icon_url(self):
        return self._add_postfix_url("icon", self.name)
    icon_url = property(_get_icon_url)
    
    def setup_icon(self):
        img_icon = Image.open(self.path).convert('RGBA')
        img_icon = auto_crop(img_icon, width=180, height=180)
        img_icon.save(self.icon_path, 'JPEG', quality=80)
        
    def setup_thumb(self):
        img_thumb = Image.open(self.path).convert('RGBA')
        img_thumb.thumbnail(
                (self.field.thumb_width, self.field.thumb_height),
                Image.ANTIALIAS
            )
        img_thumb.save(self.thumb_path, 'JPEG', quality=80)
        
    def setup_normal(self):
        img_normal = Image.open(self.path).convert('RGBA')        
        img_normal.thumbnail(
            (self.field.normal_width, self.field.normal_height),
            Image.ANTIALIAS
        )
        img_normal.save(self.normal_path, 'JPEG', quality=100)

    def save(self, name, content, save=True):
        md5 = hashlib.md5()
        md5.update(str(random.randint(10000, 90000)) + str(time.clock()))
        filebase = md5.hexdigest()
        parts = name.split(".")
        name = "%s.jpg" % (filebase)
        super(ThumbnailImageFieldFile, self).save(name, content, save)
        try:
            self.setup_icon()
            self.setup_thumb()
            self.setup_normal()
        except:
            pass
        
    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        if os.path.exists(self.normal_path):
            os.remove(self.normal_path)
        super(ThumbnailImageFieldFile, self).delete(save)
        

class ThumbnailImageField(ImageField):
    attr_class = ThumbnailImageFieldFile

    def __init__(self, *args, **kwargs):
        self.thumb_width = settings.PHOTOS_THUMB_WIDTH
        self.thumb_height = settings.PHOTOS_THUMB_HEIGHT
        self.normal_width = settings.PHOTOS_NORMAL_WIDTH
        self.normal_height = settings.PHOTOS_NORMAL_HEIGHT

        self.base_dir = "%s/%s" % (settings.MEDIA_ROOT, 'photos')
        self.base_url = "%s/%s" % (settings.MEDIA_URL, 'photos')
        
        super(ThumbnailImageField, self).__init__(*args, **kwargs)
