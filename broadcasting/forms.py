from django import forms
from tradingfeed.choices import Choices  # Import the Choices class
from .models import Broadcast, Category


class BroadcastFilterForm(forms.Form):
    search = forms.CharField(required=False, label="Search keywords")
    category = forms.ChoiceField(
        required=False,
        choices=[("", "All Categories")] + Choices.CATEGORY_CHOICES,
        label="Category",
    )
    brand = forms.CharField(required=False, label="Brand")
    condition = forms.ChoiceField(
        required=False,
        choices=[("", "All Conditions")] + Choices.CONDITION_CHOICES,
        label="Condition",
    )
    country = forms.CharField(required=False, label="Country")
    min_quantity = forms.IntegerField(required=False, label="Min quantity")
    max_quantity = forms.IntegerField(required=False, label="Max quantity")
    min_price = forms.DecimalField(
        required=False, max_digits=10, decimal_places=2, label="Min price"
    )
    max_price = forms.DecimalField(
        required=False, max_digits=10, decimal_places=2, label="Max price"
    )
    currency = forms.ChoiceField(
        required=False,
        choices=[("", "All Currencies")] + Choices.CURRENCY_CHOICES,
        label="Currency",
    )


# forms.py


class BroadcastForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100, required=False, help_text="Enter a new category if not listed"
    )
    class Meta:
        model = Broadcast
        fields = [
            "type",
            "brand",
            "title",
            "condition",
            "price",
            "quantity",
            "country",
            "source",
            "description",
            "currency",
            "category",
        ]

    def __init__(self, *args, **kwargs):
        super(BroadcastForm, self).__init__(*args, **kwargs)
        self.fields["category"] = forms.ModelChoiceField(
            queryset=Category.objects.all(),
            required=False,
            help_text="Select a category or add a new one",
        )


class BroadcastSearchForm(forms.Form):
    search = forms.CharField(required=False)
