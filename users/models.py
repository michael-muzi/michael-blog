from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import os

AVATAR_SIZES = (128, 96, 64, 48, 32, 24, 16)
GENDER_CHOICES = (('F', _('Female')), ('M', _('Male')),)


class Avatar(models.Model):
    """
    Avatar model
    """
    image = models.ImageField(upload_to="avatars/%Y/%b/%d")
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField()

    class Meta:
        unique_together = (('user', 'valid'),)

    def __unicode__(self):
        return _("%s's Avatar") % self.user

    def delete(self):
        base, filename = os.path.split(self.image.path)
        name, extension = os.path.splitext(filename)
        for key in AVATAR_SIZES:
            try:
                os.remove(os.path.join(base, "%s.%s%s" % (name, key, extension)))
            except:
                pass

        super(Avatar, self).delete()

    def save(self):
        try:
            for avatar in Avatar.objects.filter(user=self.user, valid=self.valid).exclude(id=self.id):
                base, filename = os.path.split(avatar.image.path)
                name, extension = os.path.splitext(filename)
                for key in AVATAR_SIZES:
                        os.remove(os.path.join(base, "%s.%s%s" % (name, key, extension)))
                    
                avatar.delete()
        except:
            pass

        super(Avatar, self).save()


class Profile(models.Model):
    """
    User profile model
    """
    
    user = models.OneToOneField(User)
    screenname = models.CharField(max_length=40, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    about = models.TextField(blank=True)
    figurephoto = models.CommaSeparatedIntegerField(max_length=255, blank=True)
    job = models.CharField(max_length=255, blank=True)
    declaration=models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    qq_or_msn = models.CharField(max_length=255, blank=True)

    def get_figurephoto_url(self,normal=False):
        #get full size avatar
        url = self.get_avatar_url(size=128)
        try:
            l = str(self.figurephoto).split(',')
            if len(l) > 0 and l[0]:
                photo_item = PhotoItem.objects.get(id=l[0])
                if photo_item:
                    if normal:
                        url = photo_item.image.normal_url
                    else:
                        url = photo_item.image.thumb_url
            else:
                return url
        except Exception, e:
            print e
        return url
