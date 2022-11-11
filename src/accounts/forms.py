from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from accounts.models import Comment, Profile


class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()

        fields = ["username", "password"]

    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "email"})
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "password"}),
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email", "photo", "phone_number", "address")

        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control rounded border border-success p-2 mb-2"}),
            "first_name": forms.TextInput(attrs={"class": "form-control rounded border border-success p-2 mb-2"}),
            "last_name": forms.TextInput(attrs={"class": "form-control rounded border border-success p-2 mb-2"}),
            "address": forms.TextInput(attrs={"class": "form-control rounded border border-success p-2 mb-2"}),
            "photo": forms.ClearableFileInput(
                attrs={"class": "form-control"},
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)

    comment = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={"class": "form-control form-control-lg", "placeholder": "Leave your comment here "}
        ),
    )
