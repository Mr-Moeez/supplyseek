from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def update_session(request):
    if request.method == "POST":
        plan = request.POST.get("plan")
        subscription = request.POST.get("subscription")
        price = request.POST.get("price")

        request.session["plan"] = plan
        request.session["subscription"] = subscription
        request.session["price"] = price

        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})
