from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile, UserReport


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_pic"]


class UserReportForm(forms.ModelForm):
    class Meta:
        model = UserReport
        fields = ["author", "target_user", "contact_mail", "type", "content"]
        widgets = {
            "target_user": forms.HiddenInput(),
            "author": forms.HiddenInput(),
        }
