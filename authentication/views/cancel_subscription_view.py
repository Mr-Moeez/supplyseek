from django.shortcuts import redirect
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from authentication.models import Company, CompanyUser
from subscription.models import Pricing
from userProfile.models import Profile
from django.contrib.auth.models import User


@csrf_exempt
def cancel_subscription(request):
    try:
        stripe_subscription_id = request.session.get("stripe_session_id")

        if stripe_subscription_id:
            pricing_instance = Pricing.objects.filter(
                stripe_subscription_id=stripe_subscription_id
            ).first()
            if pricing_instance:
                user = pricing_instance.user

                with transaction.atomic():
                    # Delete related data
                    Profile.objects.filter(user=user).delete()
                    CompanyUser.objects.filter(user=user).delete()
                    User.objects.filter(id=user.id).delete()
                    pricing_instance.delete()
                messages.success(
                    request, "Subscription cancelled and data rolled back successfully."
                )
            else:
                messages.error(request, "No subscription found for cancellation.")
        else:
            messages.error(request, "Invalid cancellation request.")
    except Exception as e:
        messages.error(request, "An error occurred during cancellation: " + str(e))

    return redirect("home")  # Redirect to a suitable page after cancellation
