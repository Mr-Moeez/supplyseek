from django.contrib.auth.models import User
from django.db import models
from tradingfeed.choices import Choices
from cloudinary.models import CloudinaryField


class Company(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=2)
    company_logo = CloudinaryField("image", blank=True, null=True)
    type = models.CharField(
        max_length=50, choices=Choices.BROADCAST_TYPE_CHOICES, null=True, blank=True
    )
    website = models.URLField(max_length=200, null=True, blank=True)
    other_b2b = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    registration_number = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    vat_for_eu = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(
        max_length=254, null=True, blank=True
    )
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    preferred_contact_channels = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class CompanyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"
