from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from authentication.models import Company
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class SignUpForm(UserCreationForm):  
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First name",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last name",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    email = forms.EmailField(
        max_length=150,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
                "id": "id_email",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "WhatsApp number",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Repeat password",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password1",
            "password2",
        )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Password does not match")


class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        help_text="Enter the 6-digit OTP sent to your email",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Verification code",
                "style": "border-radius: 5px; padding: 10px;"
            }
        )
    )


class CompanyForm(forms.ModelForm):
    COMPANY_TYPE_CHOICES = [
        ('EU', 'European company'),
        ('Non-EU', 'Non-European company'),
    ]

    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Company name",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    website = forms.URLField(
        max_length=200,
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": "Website (optional)",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    street = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Street",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    postal_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Postal code",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    country = CountryField(blank_label='Country').formfield(
        widget=CountrySelectWidget(
            attrs={
                "class": "form-control",
                "style": "border-radius: 5px; padding: 10px;"
            }
        )
    )
    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "State",
                "id": "id_state",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "City",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    registration_number = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Company Registration Number",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )
    
    vat = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "VAT for EU",
                "style": "border-radius: 5px; padding: 10px;",
                "disabled": "disabled"
            }
        ),
    )
    other_b2b = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Other B2B Information (optional)",
                "style": "border-radius: 5px; padding: 10px;"
            }
        ),
    )

    class Meta:
        model = Company
        fields = (
            "name",
            "website",
            "street",
            "postal_code",
            "country",
            "state",
            "city",
            "registration_number",
            "vat",
            "other_b2b",
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Company.objects.filter(name=name).exists():
            raise forms.ValidationError("Company with this name already exists.")
        return name
