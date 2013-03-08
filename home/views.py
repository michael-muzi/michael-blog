from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.template import RequestContext


def index(request, template='base.html', mimetype=None):
    data={'michael':'michael'}
    return render_to_response(template, data, mimetype=mimetype, context_instance=RequestContext(request))
