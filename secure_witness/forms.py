from django import forms
from django.contrib.auth.models import User
from secure_witness.models import UserProfile
from django.forms.models import inlineformset_factory


from secure_witness.models import (
    Folder,
    Report,
)


FolderFileFormSet = inlineformset_factory(
    Folder,
    Report,
)



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

