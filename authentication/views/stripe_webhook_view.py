import stripe
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from subscription.models import Pricing

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret = "your_stripe_webhook_secret"

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return JsonResponse({"status": "invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({"status": "invalid signature"}, status=400)

    if event["type"] == "invoice.payment_succeeded":
        handle_payment_success(event["data"]["object"])
    elif event["type"] == "invoice.payment_failed":
        handle_payment_failed(event["data"]["object"])
    elif event["type"] == "customer.subscription.deleted":
        handle_subscription_canceled(event["data"]["object"])

    return JsonResponse({"status": "success"})


def handle_payment_success(invoice):
    subscription_id = invoice["subscription"]
    try:
        pricing = Pricing.objects.get(stripe_subscription_id=subscription_id)
        pricing.status = "Active"
        pricing.save()
    except Pricing.DoesNotExist:
        pass


def handle_payment_failed(invoice):
    subscription_id = invoice["subscription"]
    try:
        pricing = Pricing.objects.get(stripe_subscription_id=subscription_id)
        pricing.status = "Past Due"
        pricing.save()
    except Pricing.DoesNotExist:
        pass


def handle_subscription_canceled(subscription):
    subscription_id = subscription["id"]
    try:
        pricing = Pricing.objects.get(stripe_subscription_id=subscription_id)
        user = pricing.user
        pricing.delete()
        user.delete()
    except Pricing.DoesNotExist:
        pass
