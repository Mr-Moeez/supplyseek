from django.db import models
from django.conf import settings
from django.utils import timezone
from tradingfeed.choices import Choices
from django.contrib.auth.models import User


class Pricing(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(
        max_length=20, choices=Choices.PLAN_CHOICES, default="BASIC"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    billing_cycle = models.CharField(
        max_length=10,
        choices=[("Monthly", "Monthly"), ("Yearly", "Yearly")],
        default="Monthly",
    )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=Choices.STATUS_CHOICES, default="Inactive"
    )
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan}"

    def save(self, *args, **kwargs):
        if self.plan == "BASIC":
            self.price = 119
        elif self.plan == "PREMIUM":
            self.price = 299
        elif self.plan == "ENTERPRISE":
            self.price = 0  # Custom pricing, might be set differently

        # Automatically set the status based on the dates
        if self.end_date and self.end_date < timezone.now().date():
            self.status = "Inactive"
        else:
            self.status = "Active"

        super().save(*args, **kwargs)
