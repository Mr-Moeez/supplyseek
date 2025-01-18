from django import forms
from ..models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "country",
            "company_logo",
            "type",
            "website",
            "other_b2b",
            "state",
            "postal_code",
            "street",
            "city",
            "registration_number",
            "description",
            "email",
            "vat_for_eu",
            "phone_number",
            "linkedin",
            "facebook",
            "instagram",
            "preferred_contact_channels",
        ]
