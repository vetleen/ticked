from datetime import datetime  

from django.utils.timezone import utc
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect
from django.template import Context, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from todotracker.models import Todo

def frontpageview (request, message=None):
    c = {}
    c.update(csrf(request))
    template = "frontpage.html"
    return render_to_response(template, c, context_instance=RequestContext(request))



#### TODO MANAGEMENT ####
@login_required(login_url='/user/loginrequired/')
def viewtodosview (request, pgnumb=1, message=None):
    #set up
    pgnumb=int(pgnumb)
    todos_per_page=16    
    
    #pickout the todos the user will need, and count how many todos the user have that can be displayed
    def getTodosToShow(pgnumb, todos_per_page):
        '''Picks out the todos the user have requested to see, 
           and returns how many todos the user have overall,
           its obviously bad with a function that does two things, 
           but I did it this way because i wanted to have a function 
           return two values and assign thse two values to two
           variables. Deal with it.'''
        #Get a list of all unticked todos ordered by date created
        users_unticked_todos = request.user.todo_set.filter(todo_is_ticked=False).order_by("-date_created")
        #Pick out only the ones we want to display
        start_point = (pgnumb*todos_per_page)-todos_per_page
        stop_point = (pgnumb*todos_per_page)
        total_todos_selected = users_unticked_todos.count()
        if total_todos_selected < stop_point:
            stop_point = total_todos_selected
        return users_unticked_todos[start_point:stop_point], total_todos_selected
    todos_to_show, total_todos_selected = getTodosToShow(pgnumb, todos_per_page)
    
    #count possible pages
    def getPossiblePages(total_todos_selected, todos_per_page):
        if total_todos_selected <= 1: #avoid dividing by zero
            pgcount = 1
        elif total_todos_selected > 1: #sets pgcount to the number of pages needed to get through all todos...
            pgcount = ((total_todos_selected-1)/todos_per_page)+1
        return pgcount
    pgcount = getPossiblePages(total_todos_selected, todos_per_page)
    
    #pagination
    def getPagination(currentPage, totalNumberOfPages): #Thanks to Kim Joar Bekkelund for helping with this: https://gist.github.com/kjbekkelund/5504010
        beforeOrAfter = 2
        if totalNumberOfPages < 5:
            start = 1
            stop = totalNumberOfPages
        else:
            start = max(1, currentPage - beforeOrAfter)
            stop = min(totalNumberOfPages, currentPage + beforeOrAfter)
        return range(start, stop + 1)
    pagi = getPagination(pgnumb, pgcount)
    
    #serve content
    c = {'todos': todos_to_show, 'pgnumb': pgnumb, 'pgcount': pgcount, 'pagi': pagi}
    c.update(csrf(request))
    template = "view_todos.html"
    return render_to_response(template, c, context_instance=RequestContext(request))

@login_required(login_url='/user/loginrequired/')
def addtodoview (request):
    headline = request.POST['headline']
    bodytext = request.POST['bodytext']
    Todo.objects.create(headline=headline, bodytext=bodytext, owner=request.user, date_created=datetime.utcnow().replace(tzinfo=utc))
    
    return redirect(viewtodosview)

@login_required(login_url='/user/loginrequired/')
def ticktodoview (request, todoid):
    todo_to_tick = Todo.objects.get(id=todoid)
    if todo_to_tick.owner == request.user:
        todo_to_tick.todo_is_ticked = True
        todo_to_tick.date_completed = datetime.utcnow().replace(tzinfo=utc)
        todo_to_tick.save()
        return redirect(viewtodosview) #add success message
    else:
        output = "Ups, it seems we tried to tick a todo that does not belong to you and had to abort, please go back and try again..."
        return HttpResponse(output)
    

@login_required(login_url='/user/loginrequired/')
def unticktodoview (request, todoid):
    todo_to_untick = Todo.objects.get(id=todoid)
    if todo_to_untick.owner == request.user:
        todo_to_untick.todo_is_ticked = False
        todo_to_untick.save()
        return redirect(viewtickedtodoview) #add success message
    else:
        output = "Ups, it seems we tried to tick a todo that does not belong to you and had to abort, please go back and try again..."
        return HttpResponse(output)

@login_required(login_url='/user/loginrequired/')
def viewtickedtodoview (request, pgnumb=1, message=None):
    #set up
    pgnumb=int(pgnumb)
    todos_per_page=16    
    
    #pickout the todos the user will need, and count how many todos the user have that can be displayed
    def getTodosToShow(pgnumb, todos_per_page):
        '''Picks out the todos the user have requested to see, 
           and returns how many todos the user have overall,
           its obviously bad with a function that does two things, 
           but I did it this way because i wanted to have a function 
           return two values and assign thse two values to two
           variables. Deal with it.'''
        #Get a list of all unticked todos ordered by date created
        users_unticked_todos = request.user.todo_set.filter(todo_is_ticked=True).order_by("-date_completed")
        #Pick out only the ones we want to display
        start_point = (pgnumb*todos_per_page)-todos_per_page
        stop_point = (pgnumb*todos_per_page)
        total_todos_selected = users_unticked_todos.count()
        if total_todos_selected < stop_point:
            stop_point = total_todos_selected
        return users_unticked_todos[start_point:stop_point], total_todos_selected
    todos_to_show, total_todos_selected = getTodosToShow(pgnumb, todos_per_page)
    
    #count possible pages
    def getPossiblePages(total_todos_selected, todos_per_page):
        if total_todos_selected <= 1: #avoid dividing by zero
            pgcount = 1
        elif total_todos_selected > 1: #sets pgcount to the number of pages needed to get through all todos...
            pgcount = ((total_todos_selected-1)/todos_per_page)+1
        return pgcount
    pgcount = getPossiblePages(total_todos_selected, todos_per_page)
    
    #pagination
    def getPagination(currentPage, totalNumberOfPages): #Thanks to Kim Joar Bekkelund for helping with this: https://gist.github.com/kjbekkelund/5504010
        beforeOrAfter = 2
        if totalNumberOfPages < 5:
            start = 1
            stop = totalNumberOfPages
        else:
            start = max(1, currentPage - beforeOrAfter)
            stop = min(totalNumberOfPages, currentPage + beforeOrAfter)
        return range(start, stop + 1)
    pagi = getPagination(pgnumb, pgcount)
    
    #serve content
    c = {'todos': todos_to_show, 'pgnumb': pgnumb, 'pgcount': pgcount, 'pagi': pagi}
    c.update(csrf(request))
    template = "view_unticked_todos.html"
    return render_to_response(template, c, context_instance=RequestContext(request))

@login_required(login_url='/user/loginrequired/')
def deletetodoview (request, todoid):
    todo_to_delete = Todo.objects.get(id=todoid)
    if todo_to_delete:
        if todo_to_delete.owner == request.user:
            todo_to_delete.delete()
            return redirect(viewtodosview) #add success message
    else:
        return redirect(viewtodosview) #add failure message
@login_required(login_url='/user/loginrequired/')
def edittodoview (request, todoid):
    todo_to_edit = Todo.objects.get(id=todoid)
    if todo_to_edit.owner == request.user:
        c = {'todo': todo_to_edit}
        c.update(csrf(request))
        template = "edit_todo.html"
        return render_to_response(template, c, context_instance=RequestContext(request))
    else:
        output = "Ups, it seems we tried to serve you a todo that does not belong to you and had to abort, please go back and try again..."
        return HttpResponse(output)

@login_required(login_url='/user/loginrequired/')
def updatetodoview (request, todoid):
    todo_to_update = Todo.objects.get(id=todoid)
    if todo_to_update.owner == request.user:
        headline=request.POST['headline']
        todo_to_update.headline = headline
        bodytext=request.POST['bodytext']
        todo_to_update.bodytext = bodytext
        todo_to_update.save()
        return redirect(viewtodosview) #add success message
    else:
        output = "Ups, it seems we tried to serve you a todo that does not belong to you and had to abort, please go back and try again..."
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

@login_required(login_url='/user/loginrequired/')
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

##@login_required(login_url='/user/loginrequired/')
##def deleteuserview (request):
##    output = "hello world"
##    return HttpResponse(output)

@login_required(login_url='/user/loginrequired/')
def changepasswordview(request):
    old_password = request.POST['old_password']
    new_password1 = request.POST['new_password']
    new_password2 = request.POST['repeat_new_password']
    if request.user.check_password(old_password):
        if new_password1 == new_password2:
            request.user.set_password(new_password1)
            request.user.save()
            #output = "Password should be reset: old_password: %s, new_password1: %s, new_password2: %s" % (old_password, new_password1, new_password2)
            #return HttpResponse(output)
            #You should probably add a success-message here..
            return redirect(frontpageview)
        else:
            output = "Good thing you had to type the password twice, because the two times you typed the new password you typed them differently. Please go back and try again."
            return HttpResponse(output)
    else:
        output = "The password you provided did not match the password stored for this user"
        return HttpResponse(output)

def loginrequiredview (request, message=None):
    c = {}
    c.update(csrf(request))
    template = "loginrequired.html"
    return render_to_response(template, c, context_instance=RequestContext(request))

