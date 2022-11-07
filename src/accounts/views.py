from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from accounts.forms import LoginForm, ProfileForm
from accounts.models import Profile
from accounts.tasks import create_user


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class LogoutUser(LoginRequiredMixin, LogoutView):
    pass


class UserProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "accounts/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy('index')
    raise_exception = True


def generate_user(request, **kwargs):
    count = kwargs.get("count")
    create_user.delay(count)
    message = "User created"
    return render(
        request,
        template_name="catalogue/generate_data.html",
        context={"title": "Generate part", "message": message},
    )
