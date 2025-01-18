# home/context_processors.py

from .models import Notification
from userProfile.models import Profile


def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        unique_notifications = {}
        
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        for notification in notifications:
            print(notification.is_read)
            if notification.is_read is False:
                alert = notification.alert
                alert_id = alert.id
                if alert_id not in unique_notifications:
                    unique_notifications[alert_id] = {
                        "alert": alert,
                        "count": Notification.objects.filter(
                            user=request.user, alert=alert, is_read=False
                        ).count(),
                        "id": notification.id,
                    }
        return {"notifications": unique_notifications.values(), "profile": profile}
    return {}
