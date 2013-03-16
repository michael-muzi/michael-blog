#coding:utf8
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from home.models import Essay, EssayType, EssayTags
from comment.models import Comment

def index(request, template='index.html', mimetype=None):
    data={}
    return render_to_response(template, data, mimetype=mimetype, context_instance=RequestContext(request))

def essay(request, template='essay/base.html', mimetype=None):
    essay_list = Essay.objects.all()
    data={'essay_list': essay_list}
    return render_to_response(template, data, mimetype=mimetype, context_instance=RequestContext(request))
    
def search(request, template='essay/base.html', tag_id=None, type_id=None, mimetype=None):
    content = request.GET.get('content',None)
    essay_list = []
    if tag_id:
        essay_tags = EssayTags.objects.get(pk = tag_id)
        essay_list = essay_tags.essay_set.all()
    elif type_id:
        essay_type = EssayType.objects.get(pk = type_id)
        essay_list = essay_type.essay_set.all()
    elif content:
        essay_list = Essay.objects.filter(Q(title__icontains=content) | Q(type__type__icontains=content))
    data={'essay_list': essay_list}
    return render_to_response(template, data, mimetype=mimetype, context_instance=RequestContext(request))
    
def essay_detail(request, template='essay/detail.html', id=None, mimetype=None):
    essay = get_object_or_404(Essay, pk=id)
    ct = ContentType.objects.get_for_model(essay)
    comments = Comment.objects.filter(content_type=ct, object_id = essay.id)
#    data = {'essay':essay}
    data = {'essay':essay,'comments':comments}
    return render_to_response(template, data, mimetype=mimetype, context_instance=RequestContext(request))
    
@login_required
def essay_write(request, template='essay/write.html', mimetype=None):
    user = request.user
    if request.method == 'POST':
        essay = Essay()
        essay.user = user
        essay.title = request.POST['title']
        essay.content = request.POST['content']
        essay_type, created = EssayType.objects.get_or_create(type=request.POST['essayType'], \
                                                              defaults={'type': request.POST['essayType']})
        essay.type = essay_type
        tags = request.POST.get('tags','').split(',')
        essay.save()
        for i in tags:
            if not i: break
            tag, created = EssayTags.objects.get_or_create(tag=i, defaults={'tag':i,'user':user})
            essay.tag.add(tag)
            tag.tagCountPlus()
        return HttpResponseRedirect('/home/')
    
    essay_type = EssayType.objects.all()
    data={'essay_type': essay_type}
    return render_to_response(template, data, mimetype=mimetype, context_instance=RequestContext(request))
    
@login_required
def essay_rm(request,id):
    user = request.user
    essay = get_object_or_404(Essay, pk=id)
    if user == essay.user:
        essay.delete()
        return Http404
    return Response()

@login_required
def essay_editor(request, id):
    pass

def about_me_view(request, template='about.html', mimetype=None):
    data = {}
    return render_to_response(template, data, mimetype=mimetype, context_instance=RequestContext(request))
