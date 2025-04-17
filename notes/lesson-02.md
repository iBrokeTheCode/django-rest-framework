# Django REST Framework - Serializers & Response objects | Browsable API

## 1. Core Concepts

- **Serializers facilitate data transformation**: They convert complex data (querysets, model instances) into native Python data types for rendering into formats like JSON. They also perform the reverse process of **deserialization**, converting incoming data back into complex Django types after validation.
- **ModelSerializers offer a shortcut**: Django REST Framework provides both a generic `Serializer` class and a `ModelSerializer` class. The `ModelSerializer` is a convenient way to create serializers that directly deal with Django models and querysets.
- **Field declaration determines output**: When defining a serializer, you specify the fields that should be included in the output of the API response. These fields correspond to fields on your Django models.
- **Validation ensures data integrity**: Serializers handle the validation of incoming data before deserialization. You can also define **field-level validation** functions within your serializer to implement custom validation logic. These functions (named `validate_<field_name>`) take the field value as input and can raise `serializers.ValidationError` if the validation fails.
- **APIView decorator for function-based views**: The `@api_view` decorator is used to define function-based views in Django REST Framework. It allows you to specify the allowed HTTP methods for a view.
- **Response object for content negotiation**: Django REST Framework provides a `Response` object that extends Django's `HttpResponse`. It supports **content negotiation**, allowing the API to return responses in different formats (e.g., JSON, HTML) based on the client's request.
- **Browsable API for development**: Django REST Framework automatically provides a **Browsable API** when using its `Response` object. This provides a user-friendly HTML representation of your API endpoints, making it easier to inspect requests and responses during development. You can explicitly request different formats like JSON by adding `format=json` to the URL.
- **Renderers control output format**: **Renderers** are responsible for converting the response data into specific media types. Django REST Framework includes renderers for JSON and the Browsable API (HTML) by default.

## 2. Resources

- [Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Serializer Fields](https://www.django-rest-framework.org/api-guide/fields/)
- [DRF Response objects](https://www.django-rest-framework.org/api-guide/responses/)
- [DRF Browsable API](https://www.django-rest-framework.org/topics/browsable-api/)

## 3. Practical Steps

1. **Install Django REST Framework**:

   Ensure `djangorestframework` is listed in your `requirements.txt` file and installed in your virtual environment.

2. **Add REST Framework to installed apps**:

   Open your project's `settings.py` file and add `'rest_framework'` to the `INSTALLED_APPS` list.

   ```python
   INSTALLED_APPS = [
       # ... other apps
       'rest_framework',
   ]
   ```

3. **Create a `serializers.py` file in your Django app**:

   Inside your application directory (e.g., `api`), create a new file named `serializers.py`.

4. **Import necessary modules in `serializers.py`**:

   Import `serializers` from `rest_framework` and the models you want to serialize.

   ```python
   from rest_framework import serializers
   from .models import Product, Order, OrderItem
   ```

5. **Define a ModelSerializer**:

   - Create a serializer class that inherits from `serializers.ModelSerializer`.
   - Define an inner `Meta` class to link the serializer to a Django model and specify the fields to be serialized.

   ```python
   class ProductSerializer(serializers.ModelSerializer):
       class Meta:
           model = Product
           fields = ('id', 'name', 'description', 'price', 'stock')

   ```

6. **Implement field-level validation (optional)**:

   Add methods named `validate_<field_name>` to your serializer class to perform custom validation for specific fields.

   ```python
   class ProductSerializer(serializers.ModelSerializer):
        # ...

       def validate_price(self, value):
           if value <= 0:
               raise serializers.ValidationError("The price must be greater than zero.")
           return value
   ```

7. **Create Django views and urls configuration**

   Create a basic JSON Response with your Products data.

   ```py
   # api/views.py
   from django.http import JsonResponse
   from .models import Product
   from .serializers import ProductSerializer


   def list_products(request):
       products = Product.objects.all()
       serializer = ProductSerializer(products, many=True)

       return JsonResponse(data={
           'data': serializer.data
       })

   ```

   ```py
   # api/urls.py
    urlpatterns = [
        path('', views.list_products, name='list_products')
    ]

    # project/urls.py
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('products/', include('api.urls', namespace='api'))
    ]
   ```

   Then run the server and go to `127.0.0.1:8000/products` to see the Response with all Products data.

8. **Create a Django view (function-based example)**:

   - In your app's `views.py` file, import necessary modules, including the `Response` object and `@api_view` decorator from `rest_framework` and your serializer.
   - Use the `@api_view(['GET'])` decorator to allow only GET requests.
   - Fetch the queryset of products.
   - Instantiate the serializer with the queryset and `many=True`.
   - Return a `Response` object with the serialized data.

     ```python
     from rest_framework.response import Response
     from rest_framework.decorators import api_view

     from .models import Product
     from .serializers import ProductSerializer

     @api_view(['GET'])
     def product_list(request):
         products = Product.objects.all()
         serializer = ProductSerializer(products, many=True)

         return Response(serializer.data)
     ```

   - Navigate to `http://127.0.0.1:8000/products/` to see the list of products in the Browsable API or in JSON format (by adding `?format=json`).

9. **Define a view to retrieve a single product**:

   - Use the `@api_view(['GET'])` decorator.
   - Accept a primary key (`pk`) as a parameter.
   - Use `get_object_or_404` to retrieve a single product instance.
   - Instantiate the serializer with the single product instance.
   - Return a `Response` object with the serialized data.

     ```python
     @api_view(['GET'])
     def product_detail(request, pk):
         product = get_object_or_404(Product, pk=pk)
         serializer = ProductSerializer(product)

         return Response(serializer.data)
     ```

10. **Define URLs in your app's `urls.py`**:

    - Create URL patterns to map URLs to your views.

      ```python
      from django.urls import path
      from . import views

      urlpatterns = [
          path('', views.product_list, name='product_list'),
          path('<int:pk>/', views.product_detail, name='list_detail')
      ]
      ```

11. **Run the Django development server**:

    ```bash
    python manage.py runserver
    ```

12. **Access the API in your browser**:

    - Navigate to `http://127.0.0.1:8000/products/1/` (replace `1` with a product ID) to see the details of a single product.
