from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect
from django.template import Context, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


def frontpageview (request, message=None):
    c = {}
    c.update(csrf(request))
    template = "frontpage.html"
    return render_to_response(template, c, context_instance=RequestContext(request))



#### TODO MANAGEMENT ####
def viewtodosview (request, pgnumb=1, message=None):
    output = "hello world"
    return HttpResponse(output)

def addtodoview (request):
    output = "hello world"
    return HttpResponse(output)

def ticktodoview (request, todoid):
    output = "hello world"
    return HttpResponse(output)

def unticktodoview (request, todoid):
    output = "hello world"
    return HttpResponse(output)

def viewtickedtodoview (request):
    output = "hello world"
    return HttpResponse(output)

def deletetodoview (request, todoid):
    output = "hello world"
    return HttpResponse(output)

def edittodoview (request, todoid):
    output = "hello world"
    return HttpResponse(output)

#### USER MANAGEMENT ####
def loginview (request):
        ## The redirects in this view should pass along a message, I have however been unable to find out how this is done except for adding it to the url ##
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(frontpageview)
        else:
            return redirect(frontpageview)
    else:
            #Should probably add a link to reset password in case it's forgotten here at some point
        return redirect(frontpageview)

def logoutview (request):
    logout(request)
    return redirect(frontpageview)

def createnewuserview (request):
    username = request.POST['email']
    password = request.POST['password']
    if User.objects.filter(username=username).count():
        output = "username is taken, you can recover your account from the menu above..."
        return HttpResponse(output)
    elif User.objects.filter(email=username).count():
        output = "username is taken, you can recover your account from the menu above..."
        return HttpResponse(output)
    else:
        #create the user
        new_user = User.objects.create_user(username=username, password=password, email=username)
        new_user.save()
        #log the user in
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(frontpageview)
            else:
                    #This shouldn't happen when you just created the user... Account is disabled..
                return redirect(frontpageview)
        else:
                #This shouldn't happen when you just created the user... Password or username is incorrect.
            return redirect(frontpageview)
@login_required
def edituserview (request):
    if request.POST['email']:
        email=request.POST['email']
        request.user.email = email
        request.user.username = email
    if request.POST['first_name']:
        first_name=request.POST['first_name']
        request.user.first_name = first_name
    if request.POST['last_name']:
        last_name=request.POST['last_name']
        request.user.last_name = last_name
    request.user.save()
    return redirect(frontpageview)

def deleteuserview (request):
    output = "hello world"
    return HttpResponse(output)
