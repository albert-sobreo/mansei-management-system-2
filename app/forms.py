from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Register

class RegisterForm(UserCreationForm):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    department = forms.CharField(required=False)

    class Meta:
        model = Register
        fields = ('password1', 'password2', 'first_name', 'last_name', 'username', 'email', 'department')