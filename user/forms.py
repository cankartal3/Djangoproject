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
            'username'  :TextInput(attrs={'class': 'input', 'placeholder':'Kullanıcı adı'}),
            'email'     : EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'İsim'}),
            'last_name' : TextInput(attrs={'class': 'input', 'placeholder': 'Soyisim'}),
        }
CITY = [
    ('Istanbul','Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir','Izmir'),
]
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone' : TextInput(attrs={'class': 'input', 'placeholder':'phone'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'address'}),
            'city': Select(attrs={'class': 'input', 'placeholder': 'phone'},choices=CITY),
            'country': TextInput(attrs={'class': 'input', 'placeholder': 'country'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
        }