from django.apps import AppConfig


class BroadcastingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "broadcasting"

    def ready(self):
        import broadcasting.signals
