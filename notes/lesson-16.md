# API Filtering in Django REST Framework using django-filter

## 1. Key Concepts:

1.  **Default Behavior and the Need for Filtering**: By default, Django REST Framework's generic list views return the entire query set for a model manager. However, it's often necessary to allow clients to select a subset of this data through filtering.
2.  **Basic Filtering with `get_queryset`**: The simplest way to filter a query set is by overriding the `get_queryset` method in a view. This allows for dynamic filtering based on request data, such as the current authenticated user.
3.  **Generic Filtering Backends**: Django REST Framework supports generic filtering backends that simplify the creation of complex searches and filters. These filters are also integrated into the browsable API and Django admin.
4.  **`django-filter` Package**: This lesson focuses on using the `django-filter` package as a filtering backend. It's a versatile package that can be used for API filtering as well as form submissions and data filtering on web pages.
5.  **Global and Per-View Filtering**: Filter backends can be set globally in the REST Framework settings (`DEFAULT_FILTER_BACKENDS`) or on a per-view or viewset basis by setting the `filter_backends` property on the view class.
6.  **Equality-Based Filtering with `filterset_fields`**: For simple equality-based filtering, you can add a `filterset_fields` attribute to a view, listing the model fields that should be filterable using URL query parameters.
7.  **Advanced Filtering with `FilterSet` Classes**: For more complex filtering, including different lookup types (e.g., greater than, less than, contains), you can define a `FilterSet` class. This class inherits from `django_filters.FilterSet` and defines the model and the fields to filter on within a `Meta` class.
8.  **Lookup Types**: Within a `FilterSet`, you can specify different lookup types for each field, such as `exact`, `contains`, `iexact`, `icontains` for string fields, and `lt`, `gt`, `range`, `exact` for numerical fields. This allows for more flexible filtering options beyond simple equality.

## 2. Resources

- [DRF Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
- [django-filter](https://django-filter.readthedocs.io/en/stable/)
- [DRF/django-filter integration](https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html)

## 3. Practical Steps:

1.  **Install `django-filter`**: Install the package using pip.
    ```
    pip install django-filter
    ```
2.  **Add `django_filters` to `INSTALLED_APPS`**: Include `'django_filters'` in your project's `settings.py` file.
    ```python
    INSTALLED_APPS = [
        # ... other apps
        'django_filters',
    ]
    ```
3.  **Set the Default Filter Backend (Global)**: In your `settings.py` file, within the `REST_FRAMEWORK` settings, add or modify the `DEFAULT_FILTER_BACKENDS` setting to include `django_filters.rest_framework.DjangoFilterBackend`.
    ```python
    REST_FRAMEWORK = {
        # Other settings
        'DEFAULT_FILTER_BACKENDS': (
            'django_filters.rest_framework.DjangoFilterBackend',
            # ...
        ),
    }
    ```
4.  **Enable Equality-Based Filtering (Simple)**: In your view, add the `filterset_fields` attribute and set it to a tuple of the field names you want to filter on for exact matches.

    ```python
    from rest_framework import generics

    class ProductListCreateView(generics.ListCreateAPIView):
        # ... other view configurations
        filterset_fields = ('name', 'price')
    ```

    With this, you can filter the API response by adding URL parameters like `?name=television` or `?price=15.99`.

5.  **Define a `FilterSet` Class (Advanced)**: Create a new file (e.g., `filters.py`) in your app and define a `FilterSet` class that inherits from `django_filters.FilterSet`. In the `Meta` class, specify the `model` and the `fields` you want to filter on.

    ```python
    # api/filters.py
    import django_filters
    from api.models import Product

    class ProductFilter(django_filters.FilterSet):
        class Meta:
            model = Product
            fields = ['name', 'price']
    ```

6.  **Use the `filterset_class` Attribute in the View**: In your view, instead of `filterset_fields`, use the `filterset_class` attribute and set it to your defined `FilterSet` class. Import the `FilterSet` class in your view file.

    ```python
    # api/views.py
    from rest_framework import generics
    from api.models import Product
    from api.serializers import ProductSerializer
    from api.filters import ProductFilter

    class ProductListCreateView(generics.ListCreateAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        filterset_class = ProductFilter
    ```

    This will still provide equality-based filtering by default.

7.  **Specify Lookup Types in the `FilterSet`**: To enable more advanced filtering (e.g., contains, greater than), modify the `fields` attribute in your `FilterSet`'s `Meta` class to be a dictionary. The keys are the field names, and the values are lists of lookup types you want to support for that field.

    ```python
    # api/filters.py
    import django_filters
    from api.models import Product

    class ProductFilter(django_filters.FilterSet):
        name = django_filters.CharFilter(lookup_expr='icontains')
        price = django_filters.RangeFilter()

        class Meta:
            model = Product
            fields = ['name', 'price']
    ```

    Alternatively, using the dictionary syntax within `Meta`:

    ```python
    # api/filters.py
    import django_filters
    from api.models import Product

    class ProductFilter(django_filters.FilterSet):
        class Meta:
            model = Product
            fields = {
                'name': ['exact', 'icontains'],
                'price': ['exact', 'lt', 'gt', 'range']
            }
    ```

    Now you can use URL parameters like `?name__icontains=digital` or `?price__gt=100` or `?price__range=10,50`.

8.  **Case-Insensitive Filtering**: To perform case-insensitive equality or contains lookups, use `iexact` instead of `exact` and `icontains` instead of `contains` in your `FilterSet` definition.
