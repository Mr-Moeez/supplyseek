from django.urls import path
from .views import (
    bookmark_broadcast,
    user_bookmarks,
    delete_bookmark,
    delete_all_bookmarks,
    export_bookmarks_csv,
)

urlpatterns = [
    path("bookmark/<int:broadcast_id>/", bookmark_broadcast, name="bookmark_broadcast"),
    path(
        "delete_bookmark/<int:broadcast_id>/", delete_bookmark, name="delete_bookmark"
    ),
    path(
        "delete_all_bookmarks/",
        delete_all_bookmarks,
        name="delete_all_bookmarks",
    ),
    path("bookmarks/", user_bookmarks, name="user_bookmarks"),
    path("export_bookmarks_csv/", export_bookmarks_csv, name="export_bookmarks_csv"),
]
