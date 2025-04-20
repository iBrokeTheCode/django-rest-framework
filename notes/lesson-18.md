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
    class InStockFilterBackend(filters.BaseFilterBackend):
        def filter_queryset(self, request, queryset, view):
            # Define your filtering logic here
            return queryset
    ```

3.  **Import the `rest_framework.filters` module.** This is necessary to inherit from the `BaseFilterBackend` class.

    ```python
    from rest_framework import filters
    ```

4.  **Inherit from the `BaseFilterBackend` class.** This establishes your class as a custom filter backend.

    ```python
    class InStockFilterBackend(filters.BaseFilterBackend):
        pass # Implementation will go here
    ```

5.  **Override the `filter_queryset` method.** This method will contain the core filtering logic.

    ```python
    class InStockFilterBackend(filters.BaseFilterBackend):
        def filter_queryset(self, request, queryset, view):
            # Filtering logic
            return queryset
    ```

6.  **Implement the filtering logic within the `filter_queryset` method.** In this example, the goal is to filter the `queryset` to include only products where the `stock` field is greater than zero. The `filter()` method of the queryset is used to achieve this.

    ```python
    class InStockFilterBackend(filters.BaseFilterBackend):
        def filter_queryset(self, request, queryset, view):
            return queryset.filter(stock__gt=0)
    ```

    - Alternatively, the `exclude()` method can be used to perform the opposite action (exclude items where stock is greater than zero).

    ```python
    class InStockFilterBackend(filters.BaseFilterBackend):
        def filter_queryset(self, request, queryset, view):
            return queryset.exclude(stock__gt=0)
    ```

7.  **Go to your `views.py` file** where your generic view is defined.

8.  **Import your custom filter backend.** Add an import statement at the top of the file to make your `InStockFilterBackend` available. Assuming your `filters.py` file is in the `api` app:

    ```python
    from api.filters import ProductFilter, InStockFilterBackend
    ```

9.  **Add your custom filter backend to the `filter_backends` list** in your generic view. This tells Django REST Framework to use your custom filtering logic.

    ```python
    from rest_framework import generics
    from .models import Product
    from .serializers import ProductSerializer
    from django_filters.rest_framework import DjangoFilterBackend
    from rest_framework import filters as drf_filters
    from api.filters import ProductFilter, InStockFilterBackend

    class ProductListView(generics.ListAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter, InStockFilterBackend]
        filterset_class = ProductFilter
        search_fields = ['name', 'description']
        ordering_fields = ['name', 'price']
    ```

10. **Test your API endpoint.** Accessing the endpoint will now automatically apply the filtering logic defined in your custom filter backend. For the `InStockFilterBackend`, only products with a `stock` count greater than zero will be returned. If the `exclude` method was used, only products with a `stock` count of zero would be returned.
