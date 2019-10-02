from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class WordCounterForm(forms.Form):

    directory_path = forms.CharField(max_length=500)
    word = forms.CharField(max_length=50)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
