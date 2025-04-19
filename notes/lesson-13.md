# Django REST Framework - Updating & Deleting Data

## 1. Core Concepts

This lesson introduces the use of **generic views** in Django REST Framework to handle update and delete operations for API endpoints. Specifically, it discusses the `DestroyAPIView` and `UpdateAPIView`, along with their corresponding mixins (`DestroyModelMixin` and `UpdateModelMixin`).

The lesson then focuses on the **`RetrieveUpdateDestroyAPIView`**, which is a composite view that combines the functionality to retrieve, update, and delete a single model instance. This view is particularly useful when you need all three operations available for a resource accessible via its ID.

A key aspect highlighted is how these generic views work with **URL parameters** to identify the specific model instance to be acted upon. The `lookup_url_kwarg` (as seen in the `ProductDetailAPIView` example, referencing `productID` in the URL) is used to fetch the correct object from the database.

The lesson emphasizes that by subclassing these generic views and associating them with a **serializer**, the framework automatically handles tasks such as:

- Fetching the relevant object based on the URL parameter.
- Deserializing incoming request data (for PUT and PATCH requests) using the serializer.
- Updating the database object with the provided data.
- Deleting the specified database object (for DELETE requests).

Furthermore, the lesson covers how to implement **permissions** on these update and delete endpoints. By overriding the `get_permissions` method, you can specify which users or groups have the authority to perform these actions. For instance, the lesson demonstrates restricting PUT and DELETE requests to administrator users using the `IsAdminUser` permission class.

## 2. Resources

- [Generic Views](https://www.django-rest-framework.org/api-guide/generic-views/)
- [Classy DRF](https://www.cdrf.co/)

## 3. Practical Steps

This section provides a step-by-step guide based on the practical application demonstrated in the lesson.

**Step 1: Modify your view to subclass `RetrieveUpdateDestroyAPIView`.**

If you currently have a view for retrieving a single object (e.g., using `RetrieveAPIView`), replace its parent class with `RetrieveUpdateDestroyAPIView`. Ensure you have the necessary imports from `rest_framework.generics`.

```python
# views.py
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id' # Assuming your URL uses 'id' to identify the product
```

**Step 2: Ensure your `urls.py` includes a dynamic path parameter for identifying the object.**

Your URL pattern should include a parameter (e.g., `product_id` or `id`) that will be used to look up the specific product.

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... other patterns ...
    path('products/<int:id>/', views.ProductDetailAPIView.as_view()),
    # ... other patterns ...
]
```

**Step 3: Test the GET request to retrieve a product by its ID.**

You should still be able to send a GET request to the specific product URL (e.g., `/api/products/1/`) and receive the product's details.

```http
GET /api/products/1/ HTTP/1.1
```

**Step 4: Send a PUT request to update a product.**

Send a PUT request to the same URL, including the data for the update in the request body as JSON. Specify the `Content-Type` as `application/json`.

```http
PUT /api/products/1/ HTTP/1.1
Content-Type: application/json

{
    "name": "Television",
    "description": "A modern television",
    "price": 500.00
    // ... other fields to update ...
}
```

A successful update will typically return a **200 OK** response with the updated product data.

**Step 5: Send a DELETE request to delete a product.**

Send a DELETE request to the product's URL.

```http
DELETE /api/products/1/ HTTP/1.1
```

A successful deletion will usually return a **204 No Content** response. Subsequent GET requests to the same URL should then indicate that the resource no longer exists.

**Step 6: Implement custom permissions to restrict update and delete access.**

Override the `get_permissions` method in your view to define permissions based on the request method.

```python
# views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from .models import Product
from .serializers import ProductSerializer

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()] # Allow anyone to retrieve (GET)
```

This example restricts PUT, PATCH, and DELETE requests to users with the `is_staff` attribute set to `True` (as `IsAdminUser` checks this). GET requests remain open to all users (`AllowAny`).

**Step 7: Test restricted access.**

Attempting to send PUT or DELETE requests without the necessary permissions (e.g., without being logged in as an admin user) will result in a **401 Unauthorized** response, indicating that authentication credentials were not provided or are invalid.

```http
DELETE /api/products/2/ HTTP/1.1
# Expected Response: 401 Unauthorized
```

**Step 8: Obtain an authentication token (if using JWT or a similar scheme).**

If your API uses token-based authentication, you'll need to obtain a valid token for an administrator user. This typically involves sending a POST request to a login endpoint with the administrator's credentials.

```http
POST /api/login/ HTTP/1.1
Content-Type: application/json

{
    "username": "admin",
    "password": "your_admin_password"
}
```

The response will contain the access token.

**Step 9: Include the authentication token in the header for authorized requests.**

For PUT and DELETE requests that require administrator permissions, add an `Authorization` header with the obtained token. The format usually follows a scheme like "Bearer <your_access_token>".

```http
PUT /api/products/2/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
    "name": "Another Updated Television"
    // ... other fields ...
}
```

With the correct token, the update or delete request will now be processed successfully.
