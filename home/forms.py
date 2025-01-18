from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]

class BroadcastSearchForm(forms.Form):
    search = forms.CharField(required=False)
