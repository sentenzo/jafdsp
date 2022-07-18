from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import *


class LoginCreatorForm(AuthenticationForm):
    username = forms.CharField(
        label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' '}))


class SingupCreatorForm(UserCreationForm):
    username = forms.CharField(
        label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': ' '}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class NewSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        # fields = '__all__'
        fields = ['title', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
        }


class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        # fields = '__all__'
        fields = ['text', ]
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
        }
