# Django REST Framework - Permissions and Testing Permissions

## 1. Key Concepts

- **Permissions determine whether a request to a Django REST Framework API should be granted or denied access**. They work alongside authentication and throttling.
- Permission checks are executed at the beginning of the view lifecycle, before any other view code is processed.
- These checks typically utilize authentication information available in `request.user` and `request.auth` to decide if the incoming request should be permitted.
- Django REST Framework provides several built-in permission classes, such as **`IsAuthenticated`**, which allows access only to authenticated users.
- Another built-in permission class is **`IsAuthenticatedOrReadOnly`**, which grants full access to authenticated users and read-only access to unauthenticated users.
- Permissions can be applied to a view by adding the **`permission_classes`** attribute to the view class. This attribute should be a list of permission classes.
- When a permission check fails, a `PermissionDenied` or `NotAuthenticated` exception is raised, and the main body of the view does not run. This results in either a **403 Forbidden** or a **401 Unauthorized** response, depending on whether authentication was attempted and failed or not attempted at all. A 403 Forbidden response is expected when an unauthenticated user tries to access an endpoint protected by `IsAuthenticated`.
- It's important to **test API endpoints with permission requirements** to ensure they function as expected. This includes verifying that authenticated users can access allowed resources and unauthenticated users are properly denied access.

## 2. Resources

- [Permissions in Django REST Framework](https://www.django-rest-framework.org/api-guide/permissions/)
- [REST Framework Status Codes](https://www.django-rest-framework.org/api-guide/status-codes/)

## 3. Practical Steps

1.  **Import necessary permission classes** from the `rest_framework.permissions` module in your `views.py` file.

    ```python
    from rest_framework import permissions
    ```

    Also can provide a default permission classes in `settings.py`

    ```py
    REST_FRAMEWORK = {
        # Other settings...
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticatedOrReadOnly",
        ],
    }
    ```

2.  **Add the `permission_classes` attribute to your view** and set it to a list containing the desired permission classes. For example, to require authentication for the `UserOrderListAPIView`:

    ```python
    from rest_framework import generics
    from .serializers import OrderSerializer
    from .models import Order
    from rest_framework import permissions

    class UserOrderListAPIView(generics.ListAPIView):
        queryset = Order.objects.all()
        serializer_class = OrderSerializer
        permission_classes = (permissions.IsAuthenticated, ) # Permissions added

        def get_queryset(self):
            qs = super().get_queryset()
            return qs.filter(user=self.request.user)
    ```

3.  **Create a test case** in your `tests.py` file, inheriting from `django.test.TestCase`. Define a `setUp` method to create necessary test data, such as users and orders [5].

    ```python
    from django.test import TestCase
    from django.urls import reverse
    from rest_framework import status
    from api.models import User, Order

    class UserOrderTestCase(TestCase):
        def setUp(self):
            self.user1 = User.objects.create_user(username='user1', password='password1')
            self.user2 = User.objects.create_user(username='user2', password='password2')
            Order.objects.create(user=self.user1)
            Order.objects.create(user=self.user2)
    ```

4.  **Write a test function to verify access for an authenticated user.**
    Log in a user using `self.client.force_login()`, reverse the URL of the protected endpoint using `reverse()`, send a GET request, and assert that the response status code is `HTTP_200_OK` (using `status` from `rest_framework`) and that the returned data contains only the orders associated with the logged-in user. Ensure your URL pattern in `urls.py` has a `name` for `reverse()` to work.

    ```python
    from django.test import TestCase
    from django.urls import reverse

    from api.models import User, Order

    class UserOrderTestCase(TestCase):
        def setUp(self):
            # ... (setup code from previous step)

        def test_user_order_endpoint_retrieves_only_the_authenticated_user_orders(self):
            user = User.objects.get(username='user2')
            self.client.force_login(user)
            response = self.client.get(reverse('api:user_orders'))

            assert response.status_code == 200

            orders = response.json()
            self.assertTrue(all(order['user'] == user.pk for order in orders))
    ```

> [!NOTE]  
> Make sure to add a `name` for your endpoint `path('user-orders/', views.UserOrderListAPIView.as_view(), name='user_orders')` and if you add and `app_name` property, you should call it in the test.

5.  **Write a test function to verify denial of access for an unauthenticated user.**
    Send a GET request to the protected endpoint without logging in any user and assert that the response status code is `HTTP_403_FORBIDDEN` (using `status` from `rest_framework`).

    ```python
    from django.test import TestCase
    from django.urls import reverse
    from rest_framework import status

    class UserOrderTestCase(TestCase):
        # ... (setup code)
        # ... (authenticated user test)

        def test_user_order_list_unauthenticated(self):
            response = self.client.get(reverse('api:user_orders'))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    ```

6.  **Import the `status` module** from `rest_framework` in your `tests.py` to use more descriptive constants for HTTP status codes, improving code readability.

    ```python
    from rest_framework import status
    ```

7.  **Use the `status` constants** (e.g., `status.HTTP_200_OK`, `status.HTTP_403_FORBIDDEN`) instead of magic numbers in your assertions. This makes your tests more understandable and maintainable.
    ```python
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    ```
