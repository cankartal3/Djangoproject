from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, FileInput, Select, PasswordInput

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
        widgets = {
            'username'  :TextInput(attrs={'class': 'vof', 'placeholder':'Kullanıcı adı'}),
            'email'     : EmailInput(attrs={'class': 'vofemail', 'placeholder': 'Email'}),
            'first_name': TextInput(attrs={'class': 'vof', 'placeholder': 'İsim'}),
            'last_name' : TextInput(attrs={'class': 'vof', 'placeholder': 'Soyisim'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone' : TextInput(attrs={'class': 'vof', 'placeholder':'phone'}),
            'address': TextInput(attrs={'class': 'vof', 'placeholder': 'address'}),
            'city': TextInput(attrs={'class': 'vof', 'placeholder': 'phone'}),
            'country': TextInput(attrs={'class': 'vof', 'placeholder': 'country'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
        }