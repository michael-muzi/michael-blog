from django.template import Variable, Library, Node, TemplateSyntaxError, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from home.models import EssayType, EssayTags

register = Library()

@register.inclusion_tag('essay/essay_right.html')
def essay_right_view():
    essay_type = EssayType.objects.all()
    essay_tags = EssayTags.objects.all()
    for type in essay_type:
        type.num = type.essay_set.all().count()
    return {'essay_type': essay_type,'essay_tags':essay_tags}