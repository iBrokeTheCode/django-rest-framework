# Django REST Framework: SearchFilter and OrderingFilter

## 1. Key Concepts

**SearchFilter:**

- The `SearchFilter` class enables simple query parameter-based searching across specified model fields.
- It is inspired by the search functionality in Django admin.
- When applied, the browsable API automatically includes a search filter control.
- To use `SearchFilter`, you need to add it to the `filter_backends` list in your generic view or viewset and define the `search_fields` attribute.
- The `search_fields` attribute should be a Python list or tuple containing the names of the model fields that you want to make searchable. The queryset associated with the view will be filtered based on these fields.
- By default, the search is performed using a case-insensitive partial match, triggered by a URL parameter named `search`.
- You can perform searches on foreign key and many-to-many fields using Django's standard double underscore (`__`) notation (e.g., `'related_model__field'`). This also works for JSON and HStore fields.
- It's possible to specify exact matches for certain fields in `search_fields` by prefixing the field name with an equals sign (`=`) (e.g., `'=name'`). In this case, only records where the field exactly matches the search term will be returned.

**OrderingFilter:**

- The `OrderingFilter` class allows clients to control the order of the results returned by the API using a query parameter.
- This is a common requirement in APIs to allow users to sort data based on different criteria.
- By default, the ordering is controlled by the `ordering` URL parameter.
- You can customize this parameter name using the `ordering_param` setting in your Django settings. Similarly, the default `search` parameter for `SearchFilter` can be changed using the `search_param` setting.
- To enable ordering, you need to add `filters.OrderingFilter` to the `filter_backends` list in your view and define the `ordering_fields` attribute.
- The `ordering_fields` attribute should be a sequence (like a list or tuple) of the model fields that clients are allowed to order the results by.
- Clients can specify the field to order by in the `ordering` parameter (e.g., `?ordering=price`). By default, the ordering is ascending.
- To order in descending order, clients can prefix the field name in the `ordering` parameter with a minus sign (`-`) (e.g., `?ordering=-price`).
- You can specify any fields from your model in `ordering_fields`, including related fields.

## 2. Resources

- [DRF Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
- [django-filter](https://django-filter.readthedocs.io/en/stable/)
- [DRF/django-filter integration](https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html)

## 3. Practical Steps

1.  **Import necessary modules from `rest_framework` and `django_filters` (if you are using `DjangoFilterBackend` as well).**

    ```python
    from rest_framework import filters
    from django_filters.rest_framework import DjangoFilterBackend
    ```

2.  **In your generic view (e.g., `ListAPIView`, `ListCreateAPIView`) or viewset, define the `filter_backends` attribute as a list and include `filters.SearchFilter` and/or `filters.OrderingFilter` along with any other filter backends you are using (like `DjangoFilterBackend`).**

    ```python
    class ProductListCreateAPIView(generics.ListCreateAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        filter_backends = (DjangoFilterBackend, filters.SearchFilter)
        # ... other configurations
    ```

3.  **If you want to enable searching, add the `search_fields` attribute to your view class. Set its value to a list or tuple of the model field names that you want to be searchable.** For example, to make the `name` and `description` fields of the `Product` model searchable:

    ```python
    class ProductListCreateAPIView(generics.ListCreateAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        filter_backends = (DjangoFilterBackend, filters.SearchFilter)
        search_fields = ('name', 'description')
        # ... other configurations
    ```

4.  **If you want to enable ordering, add the `ordering_fields` attribute to your view class. Set its value to a list or tuple of the model field names that clients are allowed to order the results by.** For example, to allow ordering by `name`, `price`, and `stock`:

    ```python
    class ProductListCreateAPIView(generics.ListCreateAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
        search_fields = ['name', 'description']
        ordering_fields = ['name', 'price', 'stock']
        # ... other configurations
    ```

5.  **Once configured, clients can use the `search` URL parameter to filter results based on the fields specified in `search_fields` (e.g., `/products/?search=Vision`). The search performs a case-insensitive partial match by default.**

6.  **Clients can use the `ordering` URL parameter to sort the results based on the fields listed in `ordering_fields` (e.g., `/products/?ordering=price` for ascending order, `/products/?ordering=-price` for descending order).**
