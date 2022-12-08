from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from accounts.forms import (CommentForm, LoginForm, ProfileForm,
                            RegistrationForm)
from accounts.models import Profile
from accounts.signup_by_email import send_registration_email
from accounts.tasks import create_user
from accounts.token import TokenGenerator
from catalogue.models import Part


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(
                    request=request,
                    template_name="accounts/login.html",
                    context={"form": form, "message": "Invalid email or password"},
                )
        else:
            return render(
                request=request,
                template_name="accounts/login.html",
                context={"form": form, "message": "Invalid email or password"},
            )

    form = LoginForm()
    return render(request=request, template_name="accounts/login.html", context={"form": form})


@login_required
def logout_user(request):
    logout(request)
    form = LoginForm()
    return render(request=request, template_name="accounts/login.html", context={"form": form})


@login_required
def update_profile(request, **kwargs):
    profile = get_object_or_404(Profile, pk=kwargs.get('pk'))
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ProfileForm(instance=profile)
    return render(request, template_name="accounts/profile.html", context={"form": form})


@login_required
def create_comment(request, **kwargs):
    if request.method == "POST":
        part = Part.objects.get(part_number=kwargs.get("part_number"))
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.part = part
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect(reverse("part_detail", args=(part.part_number,)))
    else:
        form = CommentForm()
    response = form.as_p()
    return render(request, template_name="accounts/comment.html", context={"response": response})


@login_required
def generate_user(request, **kwargs):
    if request.user.is_staff:
        count = kwargs.get("count")
        create_user.delay(count)
        message = "User created"
        return render(
            request,
            template_name="catalogue/generate_data.html",
            context={"title": "Generate part", "message": message},
        )
    else:
        return render(request,
                      template_name="core/forbidden.html",
                      context={"title": "Forbidden"})


def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_registration_email(request=request, user_instance=user)
            return render(request, template_name="accounts/sent_email_confirmation.html", context={"user": user})
        else:
            return render(request, "accounts/signup.html", {"form": form, "message": "Invalid email or password",
                                                            "password_comment": True})
    else:
        form = RegistrationForm()
    return render(request, "accounts/signup.html", {"form": form})


def activate_user(request, uuid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uuid64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        return HttpResponse("Wrong data, please retry")
    if user and TokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponse("Activation link is invalid!")
