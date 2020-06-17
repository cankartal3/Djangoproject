from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, PasswordInput


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    catid = forms.IntegerField()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )
        widgets = {
            'username': TextInput(attrs={'class': 'vof', 'placeholder': 'Kullanıcı adı'}),
            'email': EmailInput(attrs={'class': 'vofemail', 'placeholder': 'Email'}),
            'first_name': TextInput(attrs={'class': 'vof', 'placeholder': 'İsim'}),
            'last_name': TextInput(attrs={'class': 'vof', 'placeholder': 'Soyisim'}),
        }