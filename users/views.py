#coding:utf8
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os
import Image

from users.models import Avatar, Profile
from users.forms import AvatarForm
from myblog.gadget import check_and_enable_profile

DEFAULT_AVATAR = settings.DEFAULT_AVATAR

if not os.path.isfile(DEFAULT_AVATAR):
    import shutil
    image = os.path.join(os.path.abspath(os.path.dirname(__file__)),
        "python.jpg")
    shutil.copy(image, DEFAULT_AVATAR)

def register(request, template='users/register.html', mimetype=None):
    if request.method=='POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(email=email, username=username,password=password)
        user.save()
        #create profile
        check_and_enable_profile(user)
        
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect("/home/")
        return HttpResponse('not login')
    return render_to_response(template, mimetype=mimetype, context_instance=RequestContext(request))
    
def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/home/")
    else:
        # Show an error page
        return HttpResponse("password error")

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/home/")

@login_required
def upload_avatar(request):
    if not request.method == "POST":
        form = AvatarForm()
    else:
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('photo')
            avatar = Avatar(user=request.user, image=image, valid=True)
            avatar.image.save("%s.jpg" % request.user.username, image)
            image = Image.open(avatar.image.path)
            image.thumbnail((480, 480), Image.ANTIALIAS)
            image.convert("RGB").save(avatar.image.path, "JPEG")
            avatar.save()
            return HttpResponseRedirect('/home/')

    if DEFAULT_AVATAR:
        base, filename = os.path.split(DEFAULT_AVATAR)
        filename, extension = os.path.splitext(filename)
        generic96 = "%s/%s.96%s" % (base, filename, extension)
        generic96 = generic96.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
    else:
        generic96 = ""

    return HttpResponse(generic96)

def avatar(request, username, size):
    avatar = get_object_or_404(Avatar, user__username=username, valid=True).image
    avatar_path = avatar.path

    base, filename = os.path.split(avatar_path)
    name, extension = os.path.splitext(filename)
    filename = os.path.join(base, "%s.%s%s" % (name, size, extension))
    #base, temp = os.path.split(avatar.url)
    path = "%s/%s.%s%s" % (base, name, size, extension)
    if (not os.path.isfile(filename)) and os.path.isfile(avatar_path):
        try:
            image = Image.open(avatar_path)
            image.thumbnail((size, size), Image.ANTIALIAS)
            image.save(filename, "JPEG")
        except Exception, e:
            path = avatar_path
    return serve(request, path, document_root="/")

