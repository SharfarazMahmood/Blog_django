from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from app_login.models import UserProfile


class SignUpForm(UserCreationForm):
    # username = forms.EmailField(label='', required=True, widget=forms.Textarea(attrs={'placeholder': 'Username', 'rows':1}))
    # email = forms.EmailField(label='', required=True, widget=forms.Textarea(attrs={'placeholder': 'Email', 'rows':1}))
    # password1 = forms.EmailField(label='', required=True, widget=forms.Textarea(attrs={'placeholder': 'Enter a password', 'rows':1}))
    # password2 = forms.EmailField(label='', required=True, widget=forms.Textarea(attrs={'placeholder': 'Retype the password', 'rows':1}))
    email = forms.EmailField(label='Email', required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileChange(UserChangeForm):
    class Meta:
        model= User
        fields = ('username', 'email', 'first_name', 'last_name')

class ProfilePic(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic',)
