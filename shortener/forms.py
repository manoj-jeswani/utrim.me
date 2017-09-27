from django import forms
from .validators import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class submitUrlForm(forms.Form):
	url=forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Paste your url here..','class' : 'form-control'}),validators=[validate_url])

	def clean_url(self):
		got_url=self.cleaned_data['url']
		if 'http' in got_url:
			return got_url
		else:
			return 'http://'+got_url

    

 


class CustomUserCreationForm(forms.Form):
    fname= forms.CharField(label='First Name', min_length=2, max_length=150)
    lname= forms.CharField(label='Last Name', min_length=2, max_length=150)
    
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

# class LoginForm(forms.Form):
#      lusername = forms.CharField(label='Username', min_length=2, max_length=150)
#      lpassword = forms.CharField(label='Password', widget=forms.PasswordInput)

class addtobankForm(forms.Form):
    url=forms.CharField(label='',widget=forms.TextInput(attrs={'class' : 'form-control'}),validators=[validate_url])
    tag=forms.CharField(label='First Name', min_length=2, max_length=15)
    def clean_url(self):
        got_url=self.cleaned_data['url']
        if 'http' in got_url:
            return got_url
        else:
            return 'http://'+got_url



