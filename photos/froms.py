# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from photos.models import PhotoAlbum, PhotoItem

class PhotoForm(forms.Form):
    image = forms.ImageField(label=u"Выберите файл", required=True)
    descr = forms.CharField(label=u"Описание фотографии", widget=forms.Textarea, required=False)
    album = forms.ModelChoiceField(PhotoAlbum.objects.all(), required=False)
    new_album = forms.CharField(label=u"Новый альбом", required=False, max_length=255)
    
    def __init__(self, author, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['album'].queryset = self.fields['album'].queryset.filter(author=author)

    def clean_new_album(self):
        
        return self.cleaned_data['new_album']
