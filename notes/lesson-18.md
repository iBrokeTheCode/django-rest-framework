# Writing Custom Filter Backends in Django REST Framework

## 1. Key Concepts

- Django REST Framework allows developers to define **custom filter backends** to encapsulate specific filtering logic.
- To create a custom filter backend, you need to **override the base `FilterBackend` class** provided by Django REST Framework.
- The base `FilterBackend` class is located in the `rest_framework.filters` module.
- Within your custom filter backend class, you must **override the `filter_queryset` method**.
- The `filter_queryset` method should take three arguments: `request`, `queryset`, and `view`.
- This method is responsible for returning a **new filtered queryset** based on the desired logic.
- The `filter_queryset` method has access to the incoming `request`, the original `queryset` associated with the generic view, and the view itself.
- Once a custom filter backend is defined, it can be easily integrated into a generic view by adding it to the **`filter_backends` property** of that view.
- Django REST Framework will then automatically apply the filtering logic defined in the custom filter backend to the queryset before returning the response.

## 2. Resources

- [DRF Custom Generic Filtering](https://www.django-rest-framework.org/api-guide/filtering/#custom-generic-filtering)
- [DRF Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
- [django-filter](https://django-filter.readthedocs.io/en/stable/)
- [DRF/django-filter integration](https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html)

## 3. Practical Steps

1.  **Navigate to your `filters.py` file.** This is where custom filter logic is typically defined. If you don't have one, create it within your Django app.

2.  **Define a new class for your custom filter backend.** In this lesson, a filter to return only products in stock is created. The class is named `InStockFilterBackend`.

    ```python
    from rest_framework import filters

    class InStockFilter(filters.BaseFilterBackend):
        def filter_queryset(self, request, queryset, view):
            return queryset.filter(stock__gt=0)
    ```

    - Alternatively, the `exclude()` method can be used to perform the opposite action (exclude items where stock is greater than zero).

    ```python
    class InStockFilterBackend(filters.BaseFilterBackend):
        def filter_queryset(self, request, queryset, view):
            return queryset.exclude(stock__gt=0)
    ```

3.  **Go to your `views.py` file** where your generic view is defined.

4.  **Add your custom filter backend to the `filter_backends` list** in your generic view. This tells Django REST Framework to use your custom filtering logic.

    ```python
    # Other imports
    from rest_framework import filters
    from django_filters.rest_framework import DjangoFilterBackend

    from api.models import Product, Order, OrderItem
    from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductsInfoSerializer
    from api.filters import ProductFilter, InStockFilter

    class ProductListCreateAPIView(generics.ListCreateAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        filterset_class = ProductFilter
        filter_backends = (
            DjangoFilterBackend,
            filters.SearchFilter,
            filters.OrderingFilter,
            InStockFilter # Add your custom filter
        )
    ```

5.  **Test your API endpoint.** Accessing the endpoint will now automatically apply the filtering logic defined in your custom filter backend. For the `InStockFilterBackend`, only products with a `stock` count greater than zero will be returned. If the `exclude` method was used, only products with a `stock` count of zero would be returned.
