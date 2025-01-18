from django.urls import path
from .views import Pricing

app_name = "subscription_app"
urlpatterns = [
    path("", Pricing.as_view(), name="pricing"),
]
