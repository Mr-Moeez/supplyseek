from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AlertForm
from .models import Alert, AlertResult
from bookmark.models import Bookmark


@login_required
def create_alert(request):
    alerts = Alert.objects.filter(user=request.user)
    if request.method == "POST":
        form = AlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.user = request.user
            alert.save()
            messages.success(request, "Alert created successfully!")
            return render(
                request, "core/my_alerts.html", {"form": form, "alerts": alerts}
            )
    else:
        form = AlertForm()

    return render(request, "core/my_alerts.html", {"form": form, "alerts": alerts})


@login_required
def alert_results(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id, user=request.user)
    alert_results = AlertResult.objects.filter(alert=alert)
    broadcast_ids = alert_results.values_list("broadcast_id", flat=True)
    user_bookmarks = list(
        Bookmark.objects.filter(user=request.user).values_list(
            "broadcast_id", flat=True
        )
    )
    broadcast_statuses = {
        broadcast_id: broadcast_id in user_bookmarks for broadcast_id in broadcast_ids
    }
    return render(
        request,
        "core/alert_results.html",
        {
            "alert": alert,
            "alert_results": alert_results,
            "broadcast_statuses": broadcast_statuses,
        },
    )


@login_required
def delete_alert(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id, user=request.user)
    alert.delete()
    messages.success(request, "Alert deleted successfully.")
    return redirect("create_alert")
