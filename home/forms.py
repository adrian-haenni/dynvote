from home.models import UserProfile
from django.contrib.auth.models import User, Group
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)

class UserProfileForm(forms.ModelForm):

    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = UserProfile
        fields = ('picture', 'group', )