from django.contrib import admin
from .models import Company, CompanyUser

class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "type", "website")
    search_fields = ("name", "country")


class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "is_owner")
    list_filter = ("company", "is_owner")
    search_fields = ("user__username", "company__name")




admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyUser, CompanyUserAdmin)
