from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):
    """
    form responsible for registering a new user for app
    """
    class Meta:
        model=get_user_model()
        fields=('username','first_name', 'last_name', 'email','password1','password2')