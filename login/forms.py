from django import forms
from django.core.validators import RegexValidator
import datetime
from .models import *

from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm

class RegisterForm(forms.Form):
    account = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=10,required=False)
    email = forms.EmailField(max_length=50, required=False)
    password = forms.CharField(max_length=50)
