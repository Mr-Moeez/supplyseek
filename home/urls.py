from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "broadcasts/", views.home_broadcasts, name="home_broadcasts"
    ),  # This view redirects to the broadcasting view
    path("pricing/", views.pricing, name="pricing"),
    path("contact/", views.contact, name="contact"),
    path("notifications/mark_as_read/", views.mark_as_read, name="mark_as_read" ),
]
