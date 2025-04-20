import django_filters
from rest_framework import filters

from api.models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ('iexact', 'icontains'),
            'price': ('exact', 'lt', 'gt', 'range')
        }


class InStockFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
