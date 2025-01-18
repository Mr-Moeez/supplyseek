from django.urls import path
from .views import (
    BroadcastListView,
    BroadcastUpdateView,
    BroadcastDeleteView,
    broadcasts,
    broadcast_list,
    BroadcastDeleteAllView,
    ExportBroadcastsCSV,
    ImportBroadcastsView,
    BroadcastDetailsView,
)

urlpatterns = [
    path("broadcasts/", broadcasts, name="broadcasts"),
    path("my_broadcasts/", BroadcastListView.as_view(), name="my_broadcasts"),
    path(
        "add/", BroadcastListView.as_view(), name="broadcast_add"
    ),  # Use the same view to handle POST requests
    path("edit/<int:pk>/", BroadcastUpdateView.as_view(), name="broadcast_edit"),
    path("delete/<int:pk>/", BroadcastDeleteView.as_view(), name="broadcast_delete"),
    path("delete_all/", BroadcastDeleteAllView.as_view(), name="broadcast_delete_all"),
    path("export/", ExportBroadcastsCSV.as_view(), name="export_broadcasts_csv"),
    path(
        "import_broadcasts/", ImportBroadcastsView.as_view(), name="import_broadcasts"
    ),
    path(
        "details/<int:pk>/",
        BroadcastDetailsView.as_view(),
        name="broadcast_details",
    ),
]
