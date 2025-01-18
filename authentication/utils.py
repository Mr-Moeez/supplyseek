from django.conf import settings

# utils.py
import random
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp, user):
    subject = "Your OTP Code"
    context = {
        "user": user,
        "otp": otp,
    }
    html_message = render_to_string("emails/otp_email.html", context)
    plain_message = strip_tags(html_message)
    from_email = settings.SUPPORT_EMAIL
    recipient_list = [email]

    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
        fail_silently=False,
    )
