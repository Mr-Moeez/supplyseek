from django.db.models.signals import post_save
from django.dispatch import receiver
from broadcasting.models import Broadcast
from alerts.models import Alert, AlertResult
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from home.models import Notification
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_alert_email(user, broadcast, alert):
    subject = "New Broadcast Match Found!"
    context = {
        "user": user,
        "broadcast_title": broadcast.title,
        "alert": alert,
        "broadcast_url": f"http://localhost:8000/alerts/{alert.id}/",
    }
    html_message = render_to_string("emails/alert_email.html", context)
    plain_message = strip_tags(html_message)
    from_email = settings.BROADCAST_EMAIL
    recipient_list = [user.email]

    send_mail(
        subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False
    )

@receiver(post_save, sender=Broadcast)
def check_alerts_for_broadcast(sender, instance, created, **kwargs):
    if created:
        broadcast = instance
        alerts = Alert.objects.filter(
            Q(type=broadcast.type)
            | Q(category=broadcast.category)
            | Q(country=broadcast.country)
            | Q(brand=broadcast.brand)
            | Q(min_quantity__lte=broadcast.quantity)
            | Q(max_quantity__gte=broadcast.quantity)
            | Q(search__icontains=broadcast.title)
        )

        for alert in alerts:
            if (
                alert.type == broadcast.type
                and alert.condition == broadcast.condition
                and alert.category == broadcast.category
                and alert.country == broadcast.country
                and alert.brand == broadcast.brand
                and alert.min_quantity <= broadcast.quantity
                and (alert.search.lower() in broadcast.title.lower())
            ):
                alert_result, created = AlertResult.objects.get_or_create(
                    user=alert.user, alert=alert, broadcast=broadcast
                )

                if created:
                    send_alert_email(alert.user, broadcast, alert)
                    Notification.objects.create(user=alert.user, alert=alert)


