from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    class Meta:
       model=Profile
       fields=['profile_pic','bio','dob']

       widgets={
           'dob':forms.DateInput(attrs={'type':'date'})
       }
