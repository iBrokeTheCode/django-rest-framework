# Django REST Framework - Refresh Tokens & JWT Authentication

## 1. Core Concepts

- The **`TokenObtainPairView`** is accessed via the `/api/token/` endpoint. Sending a POST request to this endpoint with user credentials (username and password) returns both an **access token** and a **refresh token**.
- The **access token** is used to authenticate subsequent requests to the API by including it in the `Authorization` HTTP header. However, the access token has a limited **expiry time**. This expiry time is configurable using the Simple JWT package settings. The default expiry time for the access token is 5 minutes .
- The **refresh token** has a much longer lifespan compared to the access token; the default is one day . When an access token expires, a new one can be obtained using the refresh token.
- The **`TokenRefreshView`**, accessible via the `/api/token/refresh/` endpoint, facilitates this process. By sending a POST request to this endpoint with a valid refresh token in the request body, a new access token is issued.
- The behavior of the Simple JWT package, including the lifetime of access and refresh tokens, the algorithm used for token encryption, and the serializer classes used by the views, can be **customized through settings** . The default access token lifetime is 5 minutes, and the default refresh token lifetime is one day .

## 2. Resources

- [DRF Authentication](https://www.django-rest-framework.org/api-guide/authentication/)
- [djangorestframework-simplejwt Settings](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html)

## 3. Practical Steps

1.  **Obtain initial access and refresh tokens.**
    Send a POST request to the `/api/token/` endpoint with the user's username and password. This is typically done during the login process.

    ```
    POST /api/token/ HTTP/1.1
    Content-Type: application/json

    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

    Upon successful authentication, the response will contain an `access` token and a `refresh` token.

    ```json
    {
      "access": "your_access_token",
      "refresh": "your_refresh_token"
    }
    ```

2.  **Use the access token to access protected resources.**
    Include the `access` token in the `Authorization` header of your subsequent API requests. Typically, this is done using the Bearer schema.

3.  **Refresh the access token when it expires.**
    When the `access` token has expired, you will likely receive an authentication error from the API. At this point, you can use the `refresh` token to obtain a new `access` token. Send a POST request to the `/api/token/refresh/` endpoint with the `refresh` token in the request body.

    ```
    POST /api/token/refresh/ HTTP/1.1
    Content-Type: application/json

    {
        "refresh": "your_refresh_token"
    }
    ```

    The response will contain a new `access` token.

    ```json
    {
      "access": "a_new_access_token"
    }
    ```

    Your client application should then store this new `access` token and use it for subsequent API requests. This refresh process can be repeated as long as the `refresh` token is still valid.

4.  **Customize token lifetimes and other settings (Optional).**
    The Simple JWT package allows for customization of various settings, including the expiration times for access and refresh tokens . These settings can be configured in your Django project's `settings.py` file . For example, to change the access token lifetime to 15 minutes, you would modify the `SIMPLE_JWT` setting. Similarly, the refresh token lifetime and other parameters like the signing algorithm can also be adjusted .
