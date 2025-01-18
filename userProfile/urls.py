from django.urls import path
from .views import profile_info, company_info, security_info, public_profile

urlpatterns = [
    path("profile/profile_info", profile_info, name="profile_info"),
    path("profile/company_info", company_info, name="company_info"),
    path("profile/security_info", security_info, name="security_info"),
    path("profile/public_profile", public_profile, name="public_profile"),
]
