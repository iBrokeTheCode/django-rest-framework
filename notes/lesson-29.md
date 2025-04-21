# Testing APIs with Django REST Framework

## 1. Core Concepts

- Django REST Framework provides helper classes that extend Django's existing test framework, enhancing support for making API requests and integrating with Django REST Framework.
- The **API Request Factory** extends Django's `RequestFactory` and offers identical API methods (e.g., `get`, `post`) for creating requests. You can instantiate an `APIRequestFactory` and use it to send requests with data and specify content types like `application/json`.
- The **API Client** extends Django's native `Client` class and is used for making requests. It supports the same request interface (`get`, `post`, etc.) as Django's `Client`. The `APIClient` is the client available in Django REST Framework's test case classes.
- Django REST Framework offers test case classes that mirror existing Django test case classes. The key difference is that `self.client` on these API test case objects refers to an **API Client** instance, which is better suited for working with REST framework request and response objects. For example, `APITestCase` is provided.
- When testing API views, especially those with permissions, like the `RetrieveUpdateDestroyAPIView`, it's crucial to test different scenarios based on user roles and authentication.
- Using **named URLs** (defined using the `name` parameter in `path` in `urls.py`) is a good practice. You can then use Django's `reverse` function in your tests to refer to these URLs, which is beneficial if URL patterns change.
- In `APITestCase`, `self.client` provides methods like `get`, `post`, `put`, and `delete` for making API requests.c
- Django REST Framework's **response objects** have a `.data` attribute, which provides a convenient way to access the serialized data returned in the API response, rather than having to manually deserialize the `response.content`.
- It's important to assert the **HTTP status code** of the responses to ensure the API behaves as expected. Common status codes include 200 OK (successful GET), 401 Unauthorized (authentication required), 403 Forbidden (authenticated but not authorized), and 204 No Content (successful DELETE).
- The `rest_framework.status` module provides descriptive names for HTTP status codes (e.g., `status.HTTP_200_OK`, `status.HTTP_401_UNAUTHORIZED`), improving code readability.

## 2. Resources

- [Django Testing series](https://www.youtube.com/playlist?list=PL4cUxeGkcC9ic9O6xDW2d1qMp3rMOb0Nu)
- [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/)

## 3. Practical Steps

1.  **Import necessary modules:** In your `tests.py` file, import `reverse` from `django.urls`, your models (e.g., `User`, `Product`), `APIClient`, and `APITestCase` from `rest_framework.test`, and `status` from `rest_framework`.

    ```python
    from django.urls import reverse
    from django.contrib.auth.models import User
    from .models import Product
    from rest_framework.test import APIClient, APITestCase
    from rest_framework import status
    ```

2.  **Create a test case class:** Define a class that inherits from `APITestCase`.

    ```python
    class ProductAPITestCase(APITestCase):
        def setUp(self):
            # Setup code will go here
            pass
    ```

3.  **Implement the `setUp` method:** This method runs before each test method within the class and is used to set up common objects needed for testing, such as users and products.

    ```python
    class ProductAPITestCase(APITestCase):
        def setUp(self):
            self.admin_user = User.objects.create_superuser(
                username='admin', password='password', email='')
            self.normal_user = User.objects.create_user(
                username='user', password='password', email='')
            self.product = Product.objects.create(
                name='Test Product',
                description='Test Description',
                price=10.0,
                stock=100,
            )
            self.url = reverse('api:product_detail', kwargs={
                            'pk': self.product.pk})
    ```

4.  **Define a named URL in `urls.py`:** Ensure the URL you are testing has a `name` parameter. For example:

    ```python
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view(), name='product_detail'),
    ```

5.  **Write a test for GET requests:** Use `self.client.get(self.url)` to send a GET request to the defined URL and assert the response status code and data.

    ```python
    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], self.product.name)
    ```

    Then, run the test with the command `python manage.py test`

6.  **Write tests for unauthorized PUT and DELETE requests:** For requests that require authentication or specific permissions, send the request without proper credentials and assert that the response status code is `HTTP_401_UNAUTHORIZED`.

    ```python
    def test_unauthorized_update_product(self):
        data = {'name': 'Updated Product'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_product(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    ```

7.  **Write a test to ensure only admin users can DELETE:**

    - **Log in as a normal user** using `self.client.login(username='normal_user', password='password')`.
    - Send a DELETE request and assert that the status code is `HTTP_403_FORBIDDEN` (authorization issue) and that the product still exists in the database.
    - **Log out** using `self.client.logout()`.
    - **Log in as an admin user**.
    - Send a DELETE request and assert that the status code is `HTTP_204_NO_CONTENT` and that the product no longer exists.

    ```python
    def test_only_admins_can_delete_product(self):
        # Test that a normal user cannot delete
        self.client.login(username='user', password='password')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
        self.client.logout()

        # Test that an admin user can delete
        self.client.login(username='admin', password='password')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
    ```

8.  **Run the tests:** Use the command `python manage.py test` in your terminal to run the test suite.

This lesson emphasizes the benefits of using Django REST Framework's testing utilities for writing effective tests for your API endpoints, especially when dealing with authentication and permissions. It also highlights the convenience of `response.data` for inspecting response content.
