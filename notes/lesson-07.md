# Django REST Framework - Dynamic Filtering with get_queryset()

## 1. Core Concepts

- **Generic API Views and Querysets:** Django REST Framework's generic API views, like `ListAPIView`, utilize a `queryset` attribute to determine which objects are retrieved from the database.
- **Overriding `get_queryset()`:** Instead of directly setting the `queryset` attribute, you can override the `get_queryset()` method in your class-based views. This is necessary when you need access to the incoming request to perform dynamic filtering.
- **Dynamic Filtering based on User:** A key use case for overriding `get_queryset()` is to return data specific to the authenticated user. For example, displaying only the orders belonging to the logged-in user.
- **Accessing the Request Object:** Within the `get_queryset()` method of a class-based view (including Django REST Framework views), the `request` object is available as `self.request`.
- **Identifying the Authenticated User:** The `request` object has a `user` property (`self.request.user`) which provides access to the authenticated user.
- **Filtering the Queryset:** By accessing the authenticated user, you can filter the base queryset (obtained using `super().get_queryset()`) to include only the objects associated with that user.
- **Session-based Authentication:** The lesson demonstrates this concept using Django's built-in session-based authentication through the Django admin.

## 2. Resources

- [Generic View Methods](https://www.django-rest-framework.org/api-guide/generic-views/#methods)

## 3. Practical Steps

**Step 1: Register the Order Model with Django Admin.**

This makes the Order model manageable through the Django admin interface.

```python
# admin.py
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
```

**Step 2: Create a Superuser.**

A superuser is needed to log into the Django admin.

```bash
python manage.py createsuperuser
```

**Step 3: Start the Django Development Server.**

The server needs to be running to access the admin and API endpoints.

```bash
python manage.py runserver
```

**Step 4: Log into the Django Admin and Add Orders for Different Users.**

Log in using the created superuser and add some order entries. Notice that each order has a foreign key to a user. The lesson creates orders for a user named "John Doe" and the default "admin" user. The inlines feature allows adding order items directly when creating an order.

**Step 5: Create a New Generic API View to Filter Orders by User.**

Instead of modifying the existing `/orders` endpoint, a new view is created specifically for user-specific orders.

```python
# views.py
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
```

- A new class `UserOrderListAPIView` is created, inheriting from `generics.ListAPIView`.
- It uses the same `OrderSerializer` and a base `queryset` of all `Order` objects.
- The `get_queryset()` method is overridden.
- Inside `get_queryset()`, the authenticated `user` is accessed using `self.request.user`.
- The base `queryset` is then filtered to return only `Order` objects where the `user` field matches the authenticated `user`.

**Step 6: Define a URL for the New API View.**

A new URL pattern is added in `urls.py` to map a specific endpoint (e.g., `/user-orders/`) to the `UserOrderListAPIView`.

```python
# urls.py
from django.urls import path
from .views import OrderListAPIView, UserOrderListAPIView

urlpatterns = [
    path('orders/', OrderListAPIView.as_view()),
    path('user-orders/', UserOrderListAPIView.as_view()),
]
```

**Step 7: Test the New Endpoint.**

Accessing the `/user-orders/` endpoint will now return only the orders associated with the currently logged-in user (authenticated through the Django admin session). The lesson demonstrates that logging in as "John Doe" shows only John's orders, and logging in as "admin" shows only admin's orders.

**Step 8: Note on Authentication and Permissions.**

The lesson points out that the created `/user-orders/` endpoint is currently open to anyone, and accessing it without authentication will result in an error because `self.request.user` will not be available. The next step would be to introduce Django REST Framework permissions to require authentication for this endpoint.
