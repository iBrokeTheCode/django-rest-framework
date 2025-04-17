# Django REST Framework Generic Views

## 1. Core Concepts

- **Generic Views as Shortcuts:** Django REST Framework's generic views are designed as shortcuts for common API view patterns, allowing developers to quickly create views for common data operations without repetitive coding.
- **Class-Based Views:** This lesson transitions from function-based views to class-based views, highlighting that the latter unlock more advanced features and capabilities within Django REST Framework.
- **Abstraction of Common Patterns:** Generic views abstract common logic found in view development, enabling the composition of reusable behavior based on these classes.
- **Mapping to Database Models:** A key advantage of generic views is their ability to quickly build API views that directly correspond to your database models, especially for standard CRUD operations.
- **`ListAPIView`:** This concrete generic view is used for read-only endpoints that represent a collection of model instances. It allows you to list out all instances of a particular model.
- **`RetrieveAPIView`:** This concrete generic view is used for read-only endpoints that represent a single model instance. It allows you to retrieve a model instance by a specific parameter, often the primary key.
- **Queryset and Serializer:** When using generic views, you typically override attributes like `queryset` (to specify which model instances to operate on) and `serializer_class` (to define how data is serialized into JSON and deserialized from JSON).
- **Underlying Mechanism:** Concrete generic views like `ListAPIView` and `RetrieveAPIView` are built upon the base `GenericAPIView` and combine it with one or more mixins to provide their specific functionalities.
- **`lookup_field`:** This attribute specifies the model field used for object lookup of individual model instances and defaults to the primary key of the object.
- **`lookup_url_kwarg`:** This attribute defines the keyword argument in the URL configuration that should be used for object lookup. If unset, it defaults to the value of `lookup_field`. This allows REST framework to automatically identify how to fetch a specific object based on the URL.

## 2. Resources

- [Generic Views](https://www.django-rest-framework.org/api-guide/generic-views/)
- [DRF API Keys | HasAPIKey permission from djangorestframework-api-key](https://youtu.be/3JKAf8TQdaE?si=_WTOXHjjBrAgUucC)

## 3. Practical Steps

### Creating a `ListAPIView`

1.  **Import the `generics` module** from `rest_framework`.
    ```python
    from rest_framework import generics
    ```
2.  **Define a class** for your list view that inherits from `generics.ListAPIView`. Choose a descriptive name for your class (e.g., `ProductListAPIView`).
    ```python
    class ProductListAPIView(generics.ListAPIView):
        pass
    ```
3.  **Define the `queryset` attribute** within the class. This specifies the Django ORM queryset that the view will operate on. For example, to list all products:
    ```python
    class ProductListAPIView(generics.ListAPIView):
        queryset = Product.objects.all()
        # ...
    ```
4.  **Define the `serializer_class` attribute**. This specifies the serializer that will be used to convert the model instances to JSON.

    ```python
    from .serializers import ProductSerializer

    class ProductListAPIView(generics.ListAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
    ```

5.  **Hook up the URL** in your `urls.py` file to use this class-based view. You need to call the `.as_view()` static function on your `ListAPIView` class.

    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path('products/', views.ProductListAPIView.as_view()),
    ]
    ```

### Creating a `RetrieveAPIView`

1.  **Define a class** for your detail view that inherits from `generics.RetrieveAPIView`. Choose a descriptive name (e.g., `ProductDetailAPIView`).
    ```python
    class ProductDetailAPIView(generics.RetrieveAPIView):
        pass
    ```
2.  **Define the `queryset` attribute**. Similar to `ListAPIView`, this specifies the base queryset for retrieving single objects.
    ```python
    class ProductDetailAPIView(generics.RetrieveAPIView):
        queryset = Product.objects.all()
        # ...
    ```
3.  **Define the `serializer_class` attribute** to specify how the retrieved object should be serialized to JSON.

    ```python
    from .serializers import ProductSerializer

    class ProductDetailAPIView(generics.RetrieveAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
    ```

4.  **Hook up the URL** in your `urls.py` file. Ensure your URL pattern includes a parameter for identifying the specific object (e.g., a primary key `<pk>`). Again, use `.as_view()`.

    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),
    ]
    ```

5.  **(Optional) Customize `lookup_field`:** If you want to look up objects based on a field other than the primary key (default), you can set the `lookup_field` attribute in your view.

    ```py
    class ProductDetailAPIView(generics.RetrieveAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        lookup_field = 'name'
    ```

    And your `urls.py`:

    ```py
    path('products/<str:name>/', views.ProductDetailAPIView.as_view()),
    ```

    Now, you must access with the product's name and not the `pk`

6.  **(Optional) Customize `lookup_url_kwarg`:** If the URL parameter name doesn't match the default `pk` (for primary key lookup) or your custom `lookup_field`, you can specify the URL keyword argument using the `lookup_url_kwarg` attribute. For example, if your URL pattern uses `product_id` but your `lookup_field` is still the default `pk`:
    ```python
    class ProductDetailAPIView(generics.RetrieveAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        lookup_url_kwarg = 'product_id'
    ```
    And your `urls.py`:
    ```py
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
    ```

---

### Continues Here

### Modifying the Base `Queryset`

You can easily modify the base `queryset` in your generic view to filter the results. For example, to only return products with a stock value greater than zero:

```python
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.exclude(stock__gt=0)
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer
```

This demonstrates how generic views in Django REST Framework provide a powerful and concise way to build common API endpoints with minimal code. In future lessons, we will explore how to further customize these views and handle other HTTP methods like POST, PUT, and DELETE.
