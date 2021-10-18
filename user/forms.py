from django import forms
from django.forms import ModelForm

from user.models import User


class UserAdminForm(ModelForm):
    email = forms.CharField(disabled=True)
    name = forms.CharField(disabled=True)
    type = forms.ChoiceField(choices=User.USR_TYPE, disabled=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'type', 'is_admin', 'username']


class UsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']
