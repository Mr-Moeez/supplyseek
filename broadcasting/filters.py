import django_filters
from .models import Broadcast

class BroadcastFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Broadcast
        fields = ['type', 'brand', 'title', 'category', 'condition', 'price', 'quantity', 'country', 'source', 'date_created']

    def filter_search(self, queryset, name, value):
        keywords = value.split()
        for keyword in keywords:
            queryset = queryset.filter(
                models.Q(type__icontains=keyword) |
                models.Q(brand__icontains=keyword) |
                models.Q(title__icontains=keyword) |
                models.Q(category__icontains=keyword) |
                models.Q(condition__icontains=keyword) |
                models.Q(price__icontains=keyword) |
                models.Q(quantity__icontains=keyword) |
                models.Q(country__icontains=keyword) |
                models.Q(source__icontains=keyword) |
                models.Q(date_created__icontains=keyword)
            )
        return queryset
