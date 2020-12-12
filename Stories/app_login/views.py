from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
############ import forms for database
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordChangeForm
####### import authetication methods
from django.contrib.auth import login, authenticate, logout
##### import decorators
from django.contrib.auth.decorators import login_required
####### app custom froms
from app_login.forms import SignUpForm, UserProfileChange, ProfilePic



# Create your views here.
def sign_up(request):
    form = SignUpForm()
    registered = False
    if request.method == 'POST':
        form = SignUpForm( data=request.POST )
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


@login_required
def profile(request):
    return render(request, "app_login/profile.html", context={})


@login_required
def user_profile_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method == 'POST':
        form = UserProfileChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            return render(request, "app_login/profile.html", context={})
    dict = {'form':form}
    return render(request, "app_login/user_profile_change.html", context=dict)


@login_required
def password_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            change = False
            return render(request, "app_login/profile.html", context={})
    dict = {'form':form,
            'changed':changed}
    return render(request, "app_login/password_change.html", context=dict)



@login_required
def add_profile_pic(request):
    form = ProfilePic()
    if request.method =='POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('app_login:profile'))
    dict = {'form':form}
    return render(request, 'app_login/add_profile_pic.html', context=dict)

@login_required
def change_profile_pic(request):
    form = ProfilePic(instance=request.user.UserProfile)
    if request.method =='POST':
        form = ProfilePic(request.POST, request.FILES, instance=request.user.UserProfile)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('app_login:profile'))
    dict = {'form':form}
    return render(request, 'app_login/add_profile_pic.html', context=dict)
