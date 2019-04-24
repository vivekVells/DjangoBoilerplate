from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import User
from . import forms

userExistsStatus = False
userRef = ''


def logout(request):
    global userExistsStatus, userRef
    userExistsStatus = False
    userRef = ''
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('index')


def delSession(request):
    global userExistsStatus, userRef
    userExistsStatus = False
    userRef = ''
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponse("Session terminated...")


def login(request):
    try:
        user = User.objects.get(username=request.POST['username'])
        if user.password == request.POST['password']:
            request.session['user_id'] = user.id
            global userExistsStatus, userRef
            userExistsStatus = True
            userRef = request.POST['username']
            return True
        else:
            delSession(request)
            return False
    except User.DoesNotExist:
        delSession(request)
        return False


def home(request):
    if userExistsStatus:
        context = { 'userRef': userRef }
        return render(request, 'inspectiontaskmapper/homepage.html', context)
    else:
        return HttpResponse('Login again using the link: \'http://127.0.0.1:8000/timeclock/\' ')


def index(request):
    if request.method == 'POST':
        loginForm = forms.LoginForms()
        if loginForm.is_valid:
            if login(request):
                return redirect('home')
            else:
                context = {'form' : loginForm, 'message' : 'Username and Password didn\'t match' }
                return render(request, 'inspectiontaskmapper/index.html', context)
    else:
        delSession(request)
        loginForm = forms.LoginForms()
        context = {'form' : loginForm}
        return render(request, 'inspectiontaskmapper/index.html', context)
