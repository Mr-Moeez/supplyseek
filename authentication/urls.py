from django.urls import path
from .views.signup import check_email_availability
from .views import (
    SignUpView,
    VerifyOTPView,
    ResendOTPView,
    CompanyCreateView,
    stripe_webhook_view,
    update_session_view,
    cancel_subscription_view,
)

app_name = "authentication_app"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("verify-email/", VerifyOTPView.as_view(), name="verify_email"),
    path("resend-otp/", ResendOTPView.as_view(), name="resend_otp"),
    path("create-company/", CompanyCreateView.as_view(), name="create_company"),
    path(
        "ajax/check_email_availability/",
        check_email_availability,
        name="check_email_availability",
    ),
    path("stripe/webhook/", stripe_webhook_view.stripe_webhook, name="stripe_webhook"),
    path("update-session/", update_session_view.update_session, name="update_session"),
    path(
        "cancel-subscription/",
        cancel_subscription_view.cancel_subscription,
        name="cancel_subscription",
    ),
]
