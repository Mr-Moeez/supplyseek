from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from broadcasting.models import Broadcast  # Import Broadcast model
from .models import Bookmark
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import csv


@login_required
def bookmark_broadcast(request, broadcast_id):
    broadcast = get_object_or_404(Broadcast, id=broadcast_id)
    bookmark = Bookmark.objects.filter(user=request.user, broadcast=broadcast)
    print(broadcast_id)
    if bookmark.exists():
        bookmark.delete()
        return JsonResponse(
            {
                "status": "removed",
                "message": f"'{broadcast.title}' has been removed from your bookmarks.",
            }
        )
    else:
        Bookmark.objects.create(user=request.user, broadcast=broadcast)
        return JsonResponse(
            {
                "status": "bookmarked",
                "message": mark_safe(f"'{broadcast.title}' has been bookmarked."),
            }
        )


@login_required
def delete_bookmark(request, broadcast_id):
    broadcast = get_object_or_404(Broadcast, id=broadcast_id)
    bookmark = Bookmark.objects.filter(user=request.user, broadcast=broadcast)

    if bookmark.exists():
        bookmark.delete()
        messages.success(
            request, f"'{broadcast.title}' has been removed from your bookmarks."
        )
    else:
        messages.info(request, f"'{broadcast.title}' was not in your bookmarks.")

    return redirect("/bookmarks")


@login_required
def delete_all_bookmarks(request):

    bookmark = Bookmark.objects.all()

    if bookmark.exists():
        bookmark.delete()
        messages.success(request, f" All Bookmarks have been removed.")
    else:
        messages.info(request, f"No Bookmark available to delete.")

    return redirect("/bookmarks")


def export_bookmarks_csv(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related("broadcast")
    if not bookmarks.exists():
        messages.info(request, f"No Bookmark available to Download.")
        return redirect("/bookmarks")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="broadcasts.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "TYPE",
            "BRAND",
            "TITLE & CATEGORY",
            "CONDITION",
            "PRICE",
            "QTY",
            "COUNTRY",
            "SOURCE",
            "DATE",
        ]
    )
    for bookmark in bookmarks:
        writer.writerow(
            [
                bookmark.broadcast.get_type_display(),
                bookmark.broadcast.brand,
                f"{bookmark.broadcast.title} - {bookmark.broadcast.get_category_display()}",
                bookmark.broadcast.get_condition_display(),
                bookmark.broadcast.price,
                bookmark.broadcast.quantity,
                bookmark.broadcast.country,
                bookmark.broadcast.source,
                bookmark.broadcast.date_created.strftime("%Y-%m-%d"),
            ]
        )
    return response


@login_required
def user_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related("broadcast")
    return render(request, "core/bookmarks.html", {"bookmarks": bookmarks})
