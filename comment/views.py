#coding:utf8
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User

from comment.models import Comment
from home.models import Essay

def comment_view(request):
    contenttype = request.POST.get('content_type')
    comment = Comment()
    if contenttype == 'essay':
        object_pk = request.POST.get('object_pk')
        content_object = Essay.objects.get(id=object_pk)
        comment.content_object = content_object
        comment.nickname = request.POST.get('name')
        comment.email = request.POST.get('email')
        comment.url = request.POST.get('url')
        comment.content = request.POST.get('content')
        comment.save()
        url = '/home/essay/detail/%s/' % object_pk
        return HttpResponseRedirect(url)
    return HttpResponse('error')
