# Django REST Framework - JWT Authentication

## 1. Core Concepts

- **Authentication** is the process of associating an incoming request with identifying credentials, such as a user or a token. DRF provides various built-in authentication schemes and allows for custom implementations. Authentication runs at the beginning of a view, before permission and throttling checks.
- The DRF request object has two important properties related to authentication:
  - `request.user`: Typically set to an instance of Django's user class.
  - `request.auth`: Contains additional authentication information, such as the token used for signing the request.
- Authentication schemes are defined as a list in the `DEFAULT_AUTHENTICATION_CLASSES` setting of DRF. DRF attempts to authenticate with each class in the list and sets `request.user` and `request.auth` based on the first successful authentication. If no class authenticates, `request.user` is set to Django's anonymous user object.
- **Basic Authentication** sends an encoded username and password in the `Authorization` header. It is crucial to use HTTPS in production with Basic Authentication due to the sensitive information in the headers.
- **Session Authentication** is Django's default authentication mechanism, utilizing session IDs stored in cookies. This is used for the Django admin and the browsable API.
- **Token Authentication** is a simple DRF implementation where a token is sent in the `Authorization` header with the format `Token <token_value>`. Like Basic Authentication, it should only be used over HTTPS in production.
- **JSON Web Tokens (JWT)** are an open industry standard for securely representing claims between two parties. A key advantage of JWT authentication (as implemented by `djangorestframework-simplejwt`) over built-in token authentication is that it **doesn't require a database lookup to validate the token**. This is because the necessary information, including the user ID, is encoded within the token itself.
- The `djangorestframework-simplejwt` package is a third-party library used for JWT authentication in DRF. It generates **access tokens** and **refresh tokens**. The access token is used to authenticate requests, while the refresh token can be used to obtain a new access token when the current one expires.
- A JWT consists of three parts: a **header**, a **payload**, and a **signature**. The payload contains claims, such as the token type, expiry time, and user ID.
- **Permission classes** in DRF determine whether a successfully authenticated user has the authorization to access a specific view or perform a particular action. Examples include `IsAdminUser` (allows access only to admin users) and `IsAuthenticated` (allows access to any authenticated user).
- The **highest priority authentication class** (the first one that appears in `DEFAULT_AUTHENTICATION_CLASSES`) can influence the HTTP status code returned when authentication fails. If the highest priority class uses the `WWW-Authenticate` header, a **401 Unauthorized** response is typically returned instead of a **403 Forbidden** response when authentication fails.

## 2. Resources

- [DRF Authentication](https://www.django-rest-framework.org/api-guide/authentication/)
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [JWT](https://jwt.io/)
- [VSCode REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)
- [cURL commands](./curl-cheatsheet.md)

## 3. Practical Steps

1.  **Install the `djangorestframework-simplejwt` package** using pip:

    ```bash
    pip install djangorestframework-simplejwt
    ```

2.  **Configure `DEFAULT_AUTHENTICATION_CLASSES` in `settings.py`**: Add `'rest_framework_simplejwt.authentication.JWTAuthentication'` to the list of default authentication classes in your project's `settings.py` file. It's recommended to keep `SessionAuthentication` as a fallback, especially for accessing the Django admin interface.

    ```python
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ],
        # ... other settings
    }
    ```

    By placing `JWTAuthentication` first, it becomes the primary authentication method for your API.

3.  **Include the necessary URLs in your project's `urls.py`**: Add the URL patterns for obtaining and refreshing JWT tokens.

    ```python
    from django.urls import path
    from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

    urlpatterns = [
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        # ... your other URL patterns
    ]
    ```

    The `/api/token/` endpoint (mapped to `TokenObtainPairView`) is used to **obtain a new pair of access and refresh tokens** by providing user credentials (username and password) in the request body as JSON. The `/api/token/refresh/` endpoint (mapped to `TokenRefreshView`) is used to **obtain a new access token** by sending a valid refresh token in the request body.

4.  **Obtain JWT tokens by sending a POST request to `/api/token/`**: This request should include a JSON body with `username` and `password` keys containing valid user credentials.

    ```http
    POST /api/token/ HTTP/1.1
    Content-Type: application/json

    {
        "username": "admin",
        "password": "test"
    }
    ```

    or

    ```shell
    curl -X POST -i http://127.0.0.1:8000/api/token/ \
    -H 'Content-Type: application/json' \
    -d '{"username": "your_user", "password": "your_code"}'
    ```

    A successful response will contain an `access` token and a `refresh` token.

5.  **Authenticate subsequent requests using the access token**: Include an `Authorization` header in your HTTP requests with the value `Bearer <access_token>`, where `<access_token>` is the obtained access token (access).

    ```http
    GET /api/some_protected_endpoint/ HTTP/1.1
    Authorization: Bearer eyJh...<your_access_token>...
    ```

    or

    ```shell
    curl -X GET -i http://127.0.0.1:8000/user-orders/ \
    -H 'Authorization: Bearer <your_token>'
    ```

    DRF will then verify the JWT in the `Authorization` header to authenticate the user.

6.  **Refresh an expired access token using the refresh token**: When the access token expires, send a POST request to the `/api/token/refresh/` endpoint with a JSON body containing the `refresh` token.

    ```http
    POST /api/token/refresh/ HTTP/1.1
    Content-Type: application/json

    {
        "refresh": "<refresh-token>"
    }
    ```

    A successful response will provide a new `access` token.

7.  **Utilize permission classes to control access**: Apply permission classes to your views to enforce authorization rules based on the authenticated user. For example, to allow only admin users to create products:

    ```python
    from rest_framework import generics
    from rest_framework.permissions import IsAdminUser

    class ProductListCreateAPIView(generics.ListCreateAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer

        def get_permissions(self):
            self.permission_classes = (AllowAny,)
            if self.request.method == 'POST':
                self.permission_classes = (IsAdminUser,)
            return super().get_permissions()
    ```

    This code snippet demonstrates how to apply the `IsAdminUser` permission class specifically to POST requests for creating products.

    ```shell
    # This fails (403 Forbidden) because it's not and admin user
    curl -X POST -i http://127.0.0.1:8000/products/ \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer <token>' \
    -d '{
            "name": "Test Product",
            "price": 300.00,
            "stock": 14,
            "description": "An amazing new TV"
    }'
    ```

8.  **Handle changes in authentication failure response codes**: After setting `JWTAuthentication` as the highest priority authentication class, authentication failures on protected endpoints will likely result in a **401 Unauthorized** response instead of a 403 Forbidden response. Ensure your client-side applications and tests are adjusted to handle this change.
