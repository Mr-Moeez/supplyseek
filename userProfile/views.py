from django.shortcuts import render, redirect
from .models import Profile
from authentication.models import CompanyUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from authentication.forms.companyForm import CompanyForm


def profile_info(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
        print("Profile does not exist for this user.")

    return render(
        request, "core/profile_info.html", {"profile": profile, "active_tab": "profile"}
    )


def company_info(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
        print("Profile does not exist for this user.")

    try:
        company_user = CompanyUser.objects.get(user=user)
        company = company_user.company
    except CompanyUser.DoesNotExist:
        company_user = None
        company = None

    context = {"profile": profile, "company": company, "active_tab": "company"}

    return render(request, "core/company_info.html", context)


def security_info(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
        print("Profile does not exist for this user.")

    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("profile_info")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(
        request,
        "core/security_info.html",
        {"profile": profile, "form": form, "active_tab": "security"},
    )


def public_profile(request):
    user = request.user
    try:
        company_user = CompanyUser.objects.get(user=user)
        company = company_user.company
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
        company = None

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            if not form.cleaned_data["company_logo"]:
                company.company_logo = (
                    company_user.company.company_logo
                )  # Keep existing logo if no new file is selected
            company.save()
            return redirect("public_profile")
        else:
            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")
    else:
        form = CompanyForm(instance=company)

    return render(
        request,
        "core/public_profile_info.html",
        {
            "profile": profile,
            "form": form,
            "company": company,
            "active_tab": "public_profile",
        },
    )
