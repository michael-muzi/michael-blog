#coding:utf8
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import F


class Essay(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'))
    type = models.ForeignKey('EssayType', verbose_name=_('essay type'))
    title = models.CharField(max_length=255,null=False, verbose_name=_('title'))
    content = models.TextField(verbose_name='content', null=False, blank=False)#,null=True,blank=True)
    tag = models.ManyToManyField('EssayTags', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        
    def __unicode__(self):
        return self.title


class EssayType(models.Model):
    type = models.CharField(max_length=255, verbose_name=_('type'))
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.type


class EssayTags(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'))
    tag = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    tagCount = models.IntegerField(default=0,verbose_name=_("tag count"))
    
    def __unicode__(self):
        return self.tag
    
    def tagCountPlus(self):
        self.tagCount = F('tagCount') + 1
        self.save()
