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
            return redirect(viewtodosview)
        else:
            return redirect(frontpageview)
    else:
            #Should probably add a link to reset password in case it's forgotten here at some point
        return redirect(frontpageview)

def logoutview (request):
    output = "hello world"
    return HttpResponse(output)

def setupnewuserview (request):
    output = "hello world"
    return HttpResponse(output)

def createnewuserview (request):
    output = "hello world"
    return HttpResponse(output)

def edituserview (request):
    output = "hello world"
    return HttpResponse(output)

def deleteuserview (request):
    output = "hello world"
    return HttpResponse(output)
