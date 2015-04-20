from django import forms
from django.contrib.auth.models import User, Group
from secure_witness.models import UserProfile, Report
from django.forms.models import inlineformset_factory


from secure_witness.models import (
    Folder,
    Report,
)

"""
FolderFileFormSet = inlineformset_factory(
    Folder,
    Report,
)
"""


class ReportForm(forms.ModelForm):

    time = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y'),
        required=False)
    location = forms.CharField(required=False)
    today = forms.CharField(required=False)
    keywords = forms.CharField(required=False)
    folder = forms.ModelChoiceField(queryset=Folder.objects.all(), required=False)
    authorized_groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
        required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Report
        fields = ['folder', 'short', 'detailed', 'location', 'today', 'keywords', 'time', 'private', 'authorized_groups']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']