import re
from .models import Broadcast, Category
from bookmark.models import Bookmark
from .forms import BroadcastFilterForm, BroadcastForm, BroadcastSearchForm
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from io import TextIOWrapper
from django.views.generic.detail import DetailView
import csv

def broadcasts(request):
    broadcasts = Broadcast.objects.all()
    total_count = broadcasts.count()

    filter_form = BroadcastFilterForm(request.GET)
    search_form = BroadcastSearchForm(request.GET)
    form = BroadcastForm()

    title = request.GET.get("title")
    broadcast_type = request.GET.get("type")

    if title:
        broadcasts = broadcasts.filter(title__icontains=title)

    if broadcast_type:
        broadcasts = broadcasts.filter(type__icontains=broadcast_type)

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search", "").strip().lower()
        if search_query:
            keywords = search_query.split()
            for keyword in keywords:
                broadcasts = broadcasts.filter(
                    Q(type__icontains=keyword)
                    | Q(brand__icontains=keyword)
                    | Q(title__icontains=keyword)
                    | Q(category__icontains=keyword)
                    | Q(condition__icontains=keyword)
                    | Q(price__icontains=keyword)
                    | Q(quantity__icontains=keyword)
                    | Q(country__icontains=keyword)
                    | Q(source__icontains=keyword)
                    | Q(date_created__icontains=keyword)
                )

    if filter_form.is_valid():
        category = filter_form.cleaned_data.get("category")
        brand = filter_form.cleaned_data.get("brand")
        condition = filter_form.cleaned_data.get("condition")
        country = filter_form.cleaned_data.get("country")
        min_quantity = filter_form.cleaned_data.get("min_quantity")
        max_quantity = filter_form.cleaned_data.get("max_quantity")
        min_price = filter_form.cleaned_data.get("min_price")
        max_price = filter_form.cleaned_data.get("max_price")
        currency = filter_form.cleaned_data.get("currency")
        broadcast_type_filter = request.GET.get("type", "ALL")

        if category:
            broadcasts = broadcasts.filter(category__icontains=category)

        if brand:
            broadcasts = broadcasts.filter(brand__icontains=brand)

        if condition:
            broadcasts = broadcasts.filter(condition=condition)

        if country:
            broadcasts = broadcasts.filter(country__icontains=country)

        if min_quantity is not None:
            broadcasts = broadcasts.filter(quantity__gte=min_quantity)

        if max_quantity is not None:
            broadcasts = broadcasts.filter(quantity__lte=max_quantity)

        if min_price is not None:
            broadcasts = broadcasts.filter(price__gte=min_price)

        if max_price is not None:
            broadcasts = broadcasts.filter(price__lte=max_price)

        if currency:
            broadcasts = broadcasts.filter(currency__icontains=currency)

        if broadcast_type and broadcast_type != "ALL":
            broadcasts = broadcasts.filter(type=broadcast_type)

    if request.user.is_authenticated:
        user_bookmarks = list(
            Bookmark.objects.filter(user=request.user).values_list(
                "broadcast_id", flat=True
            )
        )
        broadcast_statuses = {
            broadcast.id: broadcast.id in user_bookmarks for broadcast in broadcasts
        }
    else:
        broadcast_statuses = {}

    context = {
        "broadcasts": broadcasts,
        "filter_form": filter_form,
        "form": form,
        "broadcast_statuses": broadcast_statuses,
        "search_form": search_form,
        "total_count": total_count

    }

    return render(request, "core/broadcasts.html", context)

def broadcast_list(request):
    query = request.GET.get('q')
    if query:
        broadcasts = Broadcast.objects.filter(title__icontains=query)  # Adjust the filter based on your model fields
    else:
        broadcasts = Broadcast.objects.all()
    
    return render(request, 'broadcasting/broadcast_list.html', {'broadcasts': broadcasts})

class BroadcastListView(LoginRequiredMixin, View):
    def get(self, request):
        broadcasts = Broadcast.objects.filter(user=request.user)
        form = BroadcastForm()
        return render(
            request, "core/my_broadcast.html", {"broadcasts": broadcasts, "form": form}
        )

    def post(self, request):
        broadcast_data = request.POST.get("broadcast_data", "")
        parsed_data = self.parse_broadcast(broadcast_data, request)

        if parsed_data:
            form = BroadcastForm(parsed_data)
        else:
            form = BroadcastForm(request.POST)

        if form.is_valid():
            broadcast = form.save(commit=False)
            broadcast.user = request.user
            new_category_name = form.cleaned_data.get("new_category")

            if new_category_name:
                category, created = Category.objects.get_or_create(
                    name=new_category_name
                )
                broadcast.category = category
            else:
                broadcast.category = form.cleaned_data["category"]

            broadcast.save()
            messages.success(request, "Broadcast created")
            return redirect("my_broadcasts")
        
        else:
            print("Form errors:", form.errors)
            messages.error(request, "There was an error creating the broadcast.")

        broadcasts = Broadcast.objects.filter(user=request.user)
        return render(
            request, "core/my_broadcast.html", {"broadcasts": broadcasts, "form": form}
        )

    def parse_broadcast(self, broadcast_data, request):
        pattern = re.compile(
            r"^Type:\s(WTS|WTB|ALL)\r?\n"
            r"Brand:\s(.+)\r?\n"
            r"Title:\s(.+)\r?\n"
            r"Category:\s(.+)\r?\n"
            r"Condition:\s(NEW|USED|ALL)\r?\n"
            r"Price:\s([\d\.]+)\s([A-Z]{3})\r?\n"
            r"Qty:\s(\d+)\r?\n"
            r"Country:\s(.+)\r?\n"
            r"Source:\s(.+)\r?\n"
            r"Description:\s(.*)$",
            re.MULTILINE,
        )
        match = pattern.match(broadcast_data.strip())

        if not match:
            messages.error(
                request, "Please make sure to match the exact pattern as shown"
            )
            return None

        (
            type,
            brand,
            title,
            category_name,
            condition,
            price,
            currency,
            quantity,
            country,
            source,
            description,
        ) = match.groups()

        category_name = category_name.strip()
        category, created = Category.objects.get_or_create(name=category_name)

        # Clean and convert the parsed data
        cleaned_data = {
            "type": type.strip(),
            "brand": brand.strip(),
            "title": title.strip(),
            "category": category,
            "condition": condition.strip(),
            "price": float(price.strip()),
            "currency": currency.strip(),
            "quantity": int(quantity.strip()),
            "country": country.strip(),
            "source": source.strip(),
            "description": description.strip() or "",
            "status": "active",
        }

        return cleaned_data


class BroadcastUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        broadcast = get_object_or_404(Broadcast, pk=pk, user=request.user)
        form = BroadcastForm(instance=broadcast)
        form_html = render_to_string(
            "core/update_broadcast.html", {"form": form}, request=request
        )
        return JsonResponse({"form_html": form_html})

    def post(self, request, pk):
        broadcast = get_object_or_404(Broadcast, pk=pk, user=request.user)
        form = BroadcastForm(request.POST, instance=broadcast)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        form_html = render_to_string(
            "core/update_broadcast.html", {"form": form}, request=request
        )
        return JsonResponse({"form_html": form_html}, status=400)


class BroadcastDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        broadcast = get_object_or_404(Broadcast, pk=pk, user=request.user)
        broadcast.delete()
        return JsonResponse({"success": True})


class BroadcastDeleteAllView(LoginRequiredMixin, View):
    def post(self, request):
        Broadcast.objects.filter(user=request.user).delete()
        return JsonResponse({"success": True})


class ExportBroadcastsCSV(View):
    def get(self, request, *args, **kwargs):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="broadcasts.csv"'

        # Create a CSV writer
        writer = csv.writer(response)

        # Write the headers
        writer.writerow(
            [
                "TYPE",
                "BRAND",
                "TITLE & CATEGORY",
                "CONDITION",
                "PRICE",
                "QTY",
                "COUNTRY",
                "SOURCE",
                "DATE",
            ]
        )

        # Filter broadcasts by the request user
        broadcasts = Broadcast.objects.filter(user=request.user)

        # Write the data
        for broadcast in broadcasts:
            writer.writerow(
                [
                    broadcast.get_type_display(),
                    broadcast.brand,
                    f"{broadcast.title} - {broadcast.get_category_display()}",
                    broadcast.get_condition_display(),
                    broadcast.price,
                    broadcast.quantity,
                    broadcast.country,
                    broadcast.source,
                    broadcast.date_created.strftime("%Y-%m-%d"),
                ]
            )

        return response


class ImportBroadcastsView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            messages.error(request, "No file uploaded.")
            return redirect("my_broadcasts")

        if not file.name.endswith(".csv"):
            messages.error(request, "Please upload a CSV file.")
            return redirect("my_broadcasts")

        try:
            csv_file = TextIOWrapper(file.file, encoding="utf-8")
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                title_category = row["TITLE & CATEGORY"].split(" - ")
                title = title_category[0]
                category = title_category[1] if len(title_category) > 1 else ""
                
                Broadcast.objects.create(
                    user=request.user,
                    type=row["TYPE"],
                    brand=row["BRAND"],
                    title=title,
                    category=category,
                    condition=row["CONDITION"],
                    price=row["PRICE"],
                    quantity=row["QTY"],
                    country=row["COUNTRY"],
                    source=row["SOURCE"],
                    date_created=row["DATE"],
                )

            messages.success(request, "Broadcasts imported successfully.")
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")

        return redirect("my_broadcasts")

class BroadcastDetailsView(DetailView):
    model = Broadcast

    def get(self, request, *args, **kwargs):
        try:
            broadcast = self.get_object()
            data = {
                "type": broadcast.get_type_display(),
                "brand": broadcast.brand,
                "title": broadcast.title,
                "category": broadcast.category.name,
                "condition": broadcast.get_condition_display(),
                "price": broadcast.price,
                "quantity": broadcast.quantity,
                "country": broadcast.country,
                "source": broadcast.source,
                "date_created": broadcast.date_created.strftime("%Y-%m-%d"),
                "status": broadcast.get_status_display(),
                "description": broadcast.description,
                "currency": broadcast.get_currency_display(),
            }
            return JsonResponse(data)
        except Broadcast.DoesNotExist:
            return JsonResponse({"error": "Broadcast not found"}, status=404)
