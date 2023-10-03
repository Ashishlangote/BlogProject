from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.validators import RegexValidator

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()


    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email', 'first_name','last_name']

class ProfileUpdateForm(forms.ModelForm):
    mobile_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = forms.CharField(validators=[mobile_regex], max_length=17)
    class Meta:
        model = Profile
        fields = ['image','mobile']