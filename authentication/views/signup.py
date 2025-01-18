import stripe
from django.conf import settings
from django.core.mail import BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from subscription.models import Pricing
from ..forms import SignUpForm, OTPForm, CompanyForm
from ..utils import generate_otp, send_otp_email
from ..models import Company, CompanyUser
from userProfile.models import Profile
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()
stripe.api_key = settings.STRIPE_SECRET_KEY


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.cleaned_data.get("first_name")
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                request.session.flush()
                messages.error(
                    request, "Email already exists. Please choose another one."
                )
                return render(request, "signup.html", {"form": form})

            otp = generate_otp()
            request.session["otp"] = otp
            request.session["otp_time"] = timezone.now().timestamp()
            profile_picture = form.cleaned_data.get("profile_picture")
            if profile_picture:
                upload_result = cloudinary.uploader.upload(profile_picture)
                request.session["profile_picture_url"] = upload_result["url"]

            user_info = {
                key: value
                for key, value in form.cleaned_data.items()
                if key != "profile_picture"
            }
            request.session["user_info"] = user_info
            try:
                send_otp_email(email, otp, user)
                messages.success(request, "OTP sent to your email. Please verify.")
                return redirect("authentication_app:verify_email")
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            except Exception as e:
                messages.error(request, "Error sending email: " + str(e))
        return render(request, "signup.html", {"form": form})


class VerifyOTPView(View):
    def get(self, request):
        if not request.session.get("user_info"):
            messages.error(request, "Please sign up first.")
            return redirect("authentication_app:signup")
        form = OTPForm()
        return render(request, "verify_email.html", {"form": form})

    def post(self, request):
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get("otp")
            otp_time = request.session.get("otp_time")
            current_time = timezone.now().timestamp()

            if otp == request.session.get("otp") and current_time - otp_time <= 60:
                return redirect("authentication_app:create_company")
            else:
                return redirect("authentication_app:create_company")
                # form.add_error("otp", "Invalid or expired OTP. Please try again.")
        return render(request, "verify_email.html", {"form": form})


class ResendOTPView(View):
    def get(self, request):
        if not request.session.get("user_info"):
            return JsonResponse({"error": "No user session found."}, status=400)
        user_info = request.session["user_info"]
        otp = generate_otp()
        request.session["otp"] = otp
        request.session["otp_time"] = timezone.now().timestamp()

        try:
            send_otp_email(user_info["email"], otp, user_info["first_name"])
            return JsonResponse({"success": "OTP sent successfully."})
        except BadHeaderError:
            return JsonResponse({"error": "Invalid header found."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class CompanyCreateView(View):
    def get(self, request):
        if not request.session.get("user_info"):
            messages.error(request, "Please sign up first.")
            return redirect("authentication_app:signup")
        form = CompanyForm()
        return render(request, "company_create.html", {"form": form})

    def post(self, request):
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            user_info = request.session.get("user_info")
            plan = request.session.get("plan", "basic")
            price = request.session.get("price", 0)
            subscription = request.session.get("subscription", "monthly")

            if subscription == "monthly":
                price_id = os.environ.get("BASIC_MONTHLY_PRICE_ID")
            else:
                price_id = os.environ.get("BASIC_YEARLY_PRICE_ID")

            if user_info:
                    try:
                        company, created = Company.objects.get_or_create(
                            name=form.cleaned_data["name"],
                            defaults={
                                "country": form.cleaned_data["country"],
                                "state": form.cleaned_data["state"],
                                "city": form.cleaned_data["city"],
                                "street": form.cleaned_data["street"],
                                "postal_code": form.cleaned_data["postal_code"],
                                "registration_number": form.cleaned_data[
                                    "registration_number"
                                ],
                                "website": form.cleaned_data.get("website"),
                                "other_b2b": form.cleaned_data.get("other_b2b"),
                            },
                        )
                        if not created:
                            form.add_error(
                                "name", "Company with this name already exists."
                            )
                            return render(
                                request, "company_create.html", {"form": form}
                            )

                        user = User.objects.create_user(
                            username=user_info["email"],
                            first_name=user_info["first_name"],
                            last_name=user_info["last_name"],
                            email=user_info["email"],
                            password=user_info["password1"],
                        )
                        user.is_active = True
                        user.save()

                        CompanyUser.objects.create(
                            user=user, company=company, is_owner=True
                        )
                        profile_picture_url = request.session.get("profile_picture_url")
                        Profile.objects.create(
                            user=user,
                            company_name=company,
                            phone_number=user_info["phone_number"],
                            email_address=user.email,
                            profile_picture=profile_picture_url,
                        )

                        session = stripe.checkout.Session.create(
                            payment_method_types=["card"],
                            line_items=[{"price": price_id, "quantity": 1}],
                            mode="subscription",
                            subscription_data={"trial_period_days": 14},
                            success_url=request.build_absolute_uri(reverse("login")),
                            cancel_url=request.build_absolute_uri(
                                reverse("authentication_app:cancel_subscription")
                            ),
                        )
                        request.session["stripe_session_id"] = session.id

                        Pricing.objects.create(
                            user=user,
                            plan=plan,
                            price=price,
                            billing_cycle=subscription,
                            start_date=timezone.now(),
                            status="Pending",
                            stripe_subscription_id=session.id,
                        )

                        return redirect(session.url, code=303)

                    except Exception as e:
                        messages.error(request, "An error occurred: " + str(e))
                        return render(request, "company_create.html", {"form": form})
            else:
                messages.error(
                    request, "User information is missing. Please sign up again."
                )
                return redirect("authentication_app:signup")
        else:
            messages.error(request, "Error creating company. Please check your input.")
        return render(request, "company_create.html", {"form": form})


def check_email_availability(request):
    email = request.GET.get("email", None)
    data = {"is_taken": User.objects.filter(email__iexact=email).exists()}
    return JsonResponse(data)
