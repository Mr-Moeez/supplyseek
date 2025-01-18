from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "phone_number", "email_address")
    search_fields = ("user__username", "company_name", "phone_number", "email_address")


admin.site.register(Profile, ProfileAdmin)
