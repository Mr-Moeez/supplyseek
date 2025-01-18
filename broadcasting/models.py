from django.db import models
from tradingfeed.choices import Choices
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Broadcast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=Choices.ALERT_TYPE_CHOICES)
    brand = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    condition = models.CharField(max_length=10, choices=Choices.CONDITION_CHOICES)
    price = models.CharField(
        max_length=50, default="ASK"
    )
    quantity = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=8, choices=Choices.STATUS_CHOICES, default=Choices.ACTIVE
    )
    description = models.TextField(blank=True)
    currency = models.CharField(
        max_length=3, choices=Choices.CURRENCY_CHOICES, default=Choices.EUR
    )

    def __str__(self):
        return f"{self.title} - {self.category}"
