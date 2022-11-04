from django.shortcuts import render
from accounts.tasks import create_user


def generate_user(request, **kwargs):
    count = kwargs.get("count")
    create_user.delay(count)
    message = "User created"
    return render(
        request,
        template_name="catalogue/generate_data.html",
        context={"title": "Generate part", "message": message},
    )
