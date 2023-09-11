from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from celery import shared_task


@shared_task()
def send_activation_email_task(uid, token, username, email):
    message = render_to_string(
        "accounts/register/activation_link.html",
        {
            "username": username,
            "host": settings.HOST,
            "uid": uid,
            "token": token
        },
    )
    send_mail(
        _("Activate your account"),
        message,
        settings.EMAIL_HOST_USER,
        (email,),
        fail_silently=True,
    )


@shared_task
def send_password_reset_email_task(context):
    message = render_to_string(
        "accounts/password_reset/email_message.html",
        context
    )
    send_mail(
        _("Reset your password"),
        message,
        settings.EMAIL_HOST_USER,
        (context["email"],),
        fail_silently=True,
    )
