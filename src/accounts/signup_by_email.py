from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.token import TokenGenerator
from config.settings.base import EMAIL_HOST_USER
from config.settings.dev import FAIL_SILENTLY


def send_registration_email(request, user_instance):
    domain = get_current_site(request)
    message = render_to_string(
        template_name="accounts/registration_email.html",
        context={
            "user": user_instance,
            "uuid": urlsafe_base64_encode(force_bytes(user_instance.pk)),
            "token": TokenGenerator().make_token(user_instance),
            "domain": domain,
        },
    )
    email = EmailMessage(
        subject="John Deere PartsOnlineStore account activation",
        body=message,
        from_email=EMAIL_HOST_USER,
        to=[f"{user_instance.email}", "alexosgt1@gmail.com"],
    )

    email.content_subtype = "html"

    email.send(FAIL_SILENTLY)
