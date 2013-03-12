from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.generic import GenericForeignKey

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.IntegerField()
    content_object = GenericForeignKey()
    nickname = models.CharField(max_length=255, verbose_name=_('username'))
    email = models.EmailField(_('email address'), blank=False)
    url = models.URLField(max_length=200, blank=True)
    content = models.TextField(verbose_name=_('comment content'))
    created = models.DateTimeField(auto_now_add=True)
