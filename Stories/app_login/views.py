from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
############ import forms for database
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
####### import authetication methods
from django.contrib.auth import login, authenticate, logout
##### import decorators
from django.contrib.auth.decorators import login_required



# Create your views here.
def sign_up(request):
    form = UserCreationForm()
    registered = False
    if request.method == 'POST':
        form = UserCreationForm( data=request.POST )
        if form.is_valid():
            form.save()
            registered = True
    dict = {'form':form, 'registered':registered}
    return render( request, 'app_login/sign_up.html', context=dict )

def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm( data=request.POST )
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            ######## use built in funtion to authenticate and login
            user = authenticate(username=username, password=password)
            ###### check id user exists
            if user is not(None) and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    dict = {'form':form}
    return render( request, 'app_login/log_in.html', context=dict )

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
