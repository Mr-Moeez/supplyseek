# views.py

from django.views.generic import TemplateView


class Pricing(TemplateView):
    template_name = "core/pricing.html"
