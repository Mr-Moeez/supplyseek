from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings
from .utils import send_contact_email
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from broadcasting.models import Broadcast
from django.template.loader import render_to_string


def home(request):
    broadcasts = Broadcast.objects.all()
    return render(request, 'core/home.html', {'broadcasts': broadcasts})


def home_broadcasts(request):
    return redirect("broadcasts")


def pricing(request):
    return render(request, "core/pricing.html")

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            subject = "New Contact Form Submission"
            message = f"""
            """

            context = {
                "name": form.cleaned_data['name'],
                "email": form.cleaned_data['email'],
                "subject": form.cleaned_data['subject'],
                "message": form.cleaned_data['message'],
            }
            html_message = render_to_string("emails/contact_email.html", context)
            recipient_list = [settings.SUPPORT_EMAIL]

            email_status = send_contact_email(subject, message, recipient_list, html_message)
            if email_status == True:
                messages.success(
                    request,
                    "Your message has been received successfully. Our team will reach out to you shortly",
                )
            else:
                messages.error(request, "Error sending email: " + str(email_status))
        else:
            messages.error(
                request,
                "There was an error in your form. Please correct it and try again.",
            )
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})

@login_required
def mark_as_read(request):
    if request.method == "GET":
        if request.method == "GET":
            all_notifications = Notification.objects.filter(
                user=request.user, is_read=False
            )
            all_notifications.update(is_read=True)

            return JsonResponse(
                {"status": "success", "message": "Notification marked as read."}
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Invalid request method."}, status=400
        )
