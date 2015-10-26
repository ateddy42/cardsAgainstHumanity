from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.GET.get('next', '/'))
    s = request.POST.get('s','')
    if not s:
        next = request.GET.get('next', '/')
        if (next == '/accounts/logout/'):
            next = '/' 
        return render(request, 'auth_login.html', {"next":next})
    # user submitted form. check valid, and log in
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    next = request.POST.get('next', '/')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(next)
    else:
        error = "Sorry, that's not a valid username or password combination"
        return render(request, 'auth_login.html', {"next":next, "error":error})

def logout(request):
    auth.logout(request)
    next = request.GET.get('next', '/')
    if (next == '/accounts/logout/'):
        next = '/'
    return render(request, 'auth_logout.html', {"next":next})

@login_required
def pwd(request):
    s = request.POST.get('s', '')
    if not s:
        return render(request, 'auth_pwd.html', {})
    old = request.POST.get('old', '')
    new = request.POST.get('new', '')
    confirm = request.POST.get('confirm', '')
    if not request.user.check_password(old):
        error = "Invalid current password"
        return render(request, 'auth_pwd.html', {"error":error})
    if not (len(new) > 0):
        error = "New password must be longer"
        return render(request, 'auth_pwd.html', {"error":error})
    if not (new == confirm):
        error = "New passwords do not match"
        return render(request, 'auth_pwd.html', {"error":error})
    request.user.set_password(new)
    request.user.save()
    # Need to authenticate user using new password
    user = auth.authenticate(username=request.user.username, password=new)
    auth.login(request, user)
    if request.user.has_usable_password():
        return render(request, 'auth_pwd.html', {"success":True})
    else:
        return render(request, 'auth_pwd.html', {"error":"FUCCCCCKKKK"})

def error(request):
    raise Http404

def robots(request):
    return HttpResponse("User-agent: *\nDisallow: /", content_type='text/plain')