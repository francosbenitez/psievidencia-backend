from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import (
    force_str,
    force_bytes,
)
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .utils import generate_token
from django.shortcuts import redirect
from apps.accounts.models import User


def send_activation_email(user, request):
    """Utility function to send activation email"""
    current_site = get_current_site(request)
    email_subject = "Activá tu cuenta"
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = generate_token.make_token(user)
    msg_html = render_to_string(
        "activate.html",
        {"user": user, "domain": current_site, "uid": uidb64, "token": token},
    )
    send_mail(
        email_subject,
        "",
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=msg_html,
        fail_silently=False,
    )


def activate_user(request, uidb64, token):
    """Utility function to activate the user"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return redirect(settings.FRONTEND_URL)
    return redirect(settings.FRONTEND_URL + "error")
