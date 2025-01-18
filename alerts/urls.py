from django.urls import path
from .views import create_alert, alert_results, delete_alert

urlpatterns = [
    path("create_alert/", create_alert, name="create_alert"),
    path("alerts/<int:alert_id>/", alert_results, name="alert_results"),
    path("alerts/<int:alert_id>/", delete_alert, name="delete_alert"),
]
