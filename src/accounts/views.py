from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from accounts.forms import CommentForm, LoginForm, ProfileForm
from accounts.models import Profile
from accounts.tasks import create_user
from catalogue.models import Part


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class LogoutUser(LoginRequiredMixin, LogoutView):
    pass


@login_required
def update_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
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


def generate_user(request, **kwargs):
    count = kwargs.get("count")
    create_user.delay(count)
    message = "User created"
    return render(
        request,
        template_name="catalogue/generate_data.html",
        context={"title": "Generate part", "message": message},
    )
