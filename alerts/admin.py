from django.contrib import admin

from .models import Alert, AlertResult

admin.site.register(Alert)
admin.site.register(AlertResult)
