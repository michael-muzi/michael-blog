from django import forms
from django.utils.translation import ugettext_lazy as _


class AvatarForm(forms.Form):
    """
    The avatar form requires only one image field.
    """
    photo = forms.ImageField(required=False)
    url = forms.URLField(required=False)

    def clean_url(self):
        url = self.cleaned_data.get('url')
#        if not url: return ''
#        filename, headers = urllib.urlretrieve(url)
#        if not mimetypes.guess_all_extensions(headers.get('Content-Type')):
#            raise forms.ValidationError(_('The file type is invalid: %s' % type))
#        return SimpleUploadedFile(filename, open(filename).read(), content_type=headers.get('Content-Type'))

    def clean(self):
        if not (self.cleaned_data.get('photo')):
            raise forms.ValidationError(_('You must enter one of the options'))
        return self.cleaned_data
    