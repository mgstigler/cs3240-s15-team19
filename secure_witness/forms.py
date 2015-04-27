from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from secure_witness.models import UserProfile, Report
from django.forms.models import inlineformset_factory


from secure_witness.models import (
    Folder,
    Report,
)


class ReportForm(forms.ModelForm):

    time = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y'),
        required=False)
    location = forms.CharField(required=False)
    today = forms.CharField(required=False)
    keywords = forms.CharField(required=False)
    folder = forms.ModelChoiceField(queryset=Folder.objects.all(), required=False)
    # Display all groups except admin group
    authorized_groups = forms.ModelMultipleChoiceField(queryset=Group.objects.filter(~Q(name='admins')),
        required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Report
        fields = ['folder', 'short', 'detailed', 'location', 'today', 'keywords', 'time', 'private', 'authorized_groups']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder' : 'Email address'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def clean_email(self):
        email = self.cleaned_data["email"]
        # If no user exists, then the email is valid
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        # Otherwise, raise an exception
        raise forms.ValidationError('Duplicate Email')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.is_active = False
            user.save()

        return user

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']