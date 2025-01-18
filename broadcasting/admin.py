from django.contrib import admin
from .models import Broadcast, Category

@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ('type', 'brand', 'title', 'category', 'condition', 'price', 'quantity', 'country', 'source', 'date_created')

admin.site.register(Category)
