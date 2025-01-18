from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from tradingfeed.choices import Choices
from broadcasting.models import Broadcast


class Alert(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    search = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, choices=Choices.CATEGORY_CHOICES)
    country = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    min_quantity = models.PositiveIntegerField(default=1)
    max_quantity = models.PositiveIntegerField(blank=True, null=True)
    min_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    currency = models.CharField(
        max_length=3, choices=Choices.CURRENCY_CHOICES, default=Choices.EUR
    )
    type = models.CharField(
        max_length=3, choices=Choices.ALERT_TYPE_CHOICES, default=Choices.ALL
    )
    condition = models.CharField(
        max_length=4, choices=Choices.CONDITION_CHOICES, default=Choices.ALL
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    frequency = models.CharField(
        max_length=7, choices=Choices.FREQUENCY_CHOICE, default=Choices.ASAP
    )
    expiry_date = models.DateField(blank=True, null=True) 
    notification_channel = models.CharField(max_length=100, default="email")

    class Meta:
        indexes = [
            models.Index(fields=["user", "category"]),
        ]
        # ensure no alert could be ablle to generate with same values
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "search",
                    "category",
                    "country",
                    "brand",
                    "min_quantity",
                    "max_quantity",
                    "min_price",
                    "max_price",
                    "type",
                    "condition",
                    "name",
                ],
                name="unique_alert",
            ),
        ]

    def __str__(self):
        return f"Alert for {self.user.username} - {self.category}"

    def save(self, *args, **kwargs):
        if self.user.alert_set.count() >= 5:
            raise ValueError("You can only create up to 5 alerts.")
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self.max_quantity is not None and self.max_quantity < self.min_quantity:
            raise ValidationError(
                "Max quantity must be greater than or equal to min quantity."
            )
        if self.max_price is not None and self.max_price < self.min_price:
            raise ValidationError(
                "Max price must be greater than or equal to min price."
            )


class AlertResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    broadcast = models.ForeignKey(Broadcast, on_delete=models.CASCADE)
    date_matched = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.broadcast.title} matched with {self.alert.category}"
