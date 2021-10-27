from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, TextInput, NumberInput
from .forms import *
from .models import *
from django.forms import ModelForm

class Registrationform(UserCreationForm):
    email = forms.EmailField()
    GENDER = (
        ("M","Male"),
        ("O","Other"),
        ("F","Female")
    )
    gender = forms.ChoiceField(choices = GENDER)

    class Meta:
        model = User
        fields = ["username", "email","password1","password2","gender"]

class VehicleHistorySearchForm(forms.ModelForm):
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    class Meta:
        model = Trip
        fields = ['start_date','end_date']



class TripsForm(ModelForm):
    class Meta:
        model = Trip
        fields = ['driver',]
        widgets = {
            'driver': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'First Name'
                }),
        }

class UpdateForm(ModelForm):
    class Meta:
        model = Trip
        exclude = ('trip_date','officer','username','car_reg_number','driver','destination','purpose','passengers','time_out','time_in') 
