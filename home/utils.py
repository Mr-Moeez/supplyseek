from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def send_contact_email(subject, message, recipient_list, html_message):
    try:
        result = send_mail(
            subject,
            message,
            settings.INFO_EMAIL,
            recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        logger.debug(f"send_mail result: {result}")
        return True
    except BadHeaderError:
        logger.error("Invalid header found.")
        return HttpResponse("Invalid header found.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return HttpResponse(f"An error occurred: {e}")
