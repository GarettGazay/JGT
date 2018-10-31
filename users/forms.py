from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from multiselectfield import MultiSelectField
from .models import Profile

class UserRegisterForm(UserCreationForm):
    ORGS = (
    ('Select One','Select One'),
    ('Santa Clara Family Health Plan','Santa Clara Family Health Plan'),
    ('Valley Medical Center','Valley Medical Center'),
    ('Herman Healthcare', 'Herman Healthcare'),
    ('JustGo Drivers','JustGo Drivers'),
    )

    email=forms.EmailField(required=True)
    organization=forms.CharField(label='Organization', widget=forms.Select(choices=ORGS))

    class Meta:
        model = User
        fields = ['username', 'email', 'organization', 'password1','password2']

    def save(self,commit = True):
        user = super(UserRegisterForm, self).save(commit = False)
        user.first_name = self.cleaned_data['organization']
        if commit:
            user.save()

        return user

class UserUpdateForm(forms.ModelForm):
    ORGS = (
    ('Select One','Select One'),
    ('Santa Clara Family Health Plan','Santa Clara Family Health Plan'),
    ('Valley Medical Center','Valley Medical Center'),
    ('JustGo Drivers','JustGo Drivers'),
    )

    email = forms.EmailField()
    organization=forms.CharField(label='Organization.', widget=forms.Select(choices=ORGS))


    class Meta:
        model = User
        fields = ['username', 'email', 'organization']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
