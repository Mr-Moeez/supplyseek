from django import forms
from .models import Alert


class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = [
            "name",
            "frequency",
            "expiry_date",
            "notification_channel",
            "search",
            "category",
            "country",
            "brand",
            "min_quantity",
            "max_quantity",
            "min_price",
            "max_price",
            "currency",
            "type",
            "condition",
        ]
