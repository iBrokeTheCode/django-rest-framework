# Django & Redis - Vary Headers to Control Caching Behavior

## 1. Core Concepts

This lesson builds upon previous concepts of caching in Django using the `@cache_page` decorator and Redis. The core idea introduced is the use of **`Vary` headers** to handle scenarios where the response of a page depends on specific request headers, such as the `Authorization` header used for authentication.

By default, Django's cache system creates cache keys based on the full URL, including query parameters. This means that requests to the same URL will always receive the same cached response, regardless of differences in headers like user agent, cookies, or language preferences. This becomes a problem when the content of a page varies based on these headers, for example, displaying different orders for different authenticated users on the `/orders` endpoint.

To address this, Django provides decorators like `@vary_on_headers` (and `@vary_on_cookie`). The `@vary_on_headers` decorator allows you to specify which request headers the caching mechanism should consider when building the cache key. By using `@vary_on_headers('Authorization')`, the cache will store different versions of the response for different values of the `Authorization` header. This enables **per-user caching**, where each user's specific response is cached separately.

While `Vary` headers solve the issue of serving the wrong cached content to different users, they can also lead to a larger number of cache entries if the header values change frequently (e.g., short-lived JWT tokens). Additionally, invalidating these caches can be more complex because the cache key depends on the header value, which might not be easily accessible in model signals. Lower-level caching with user-specific key prefixes is suggested as a potential alternative for easier invalidation.

## 2. Resources

- [Vary Headers](https://docs.djangoproject.com/en/5.1/topics/http/decorators/#vary-headers)
- [DRF Caching](https://www.django-rest-framework.org/api-guide/caching/)
- [django-redis](https://github.com/jazzband/django-redis)
- [DRF - JWT Authentication with djangorestframework-simplejwt](https://youtu.be/Xp0-Yy5ow5k?si=Ze0PEuXzu5mk89DT)

## 3. Practical Steps

1.  **Initial Request (User 1):** A GET request is sent to the `/orders` endpoint with the authentication token for user 1. The response contains the orders specific to user 1.

    ```http
    GET /api/orders/
    Authorization: Bearer <user_1_jwt_token>
    ```

2.  **Request with Different User (User 2):** The authentication token is changed to that of user 2, and the same GET request to `/orders` is sent. The response now contains the orders specific to user 2.

    ```http
    GET /api/orders/
    Authorization: Bearer <user_2_jwt_token>
    ```

3.  **Implementing `@cache_page`:** The `@cache_page` decorator is added to the `list` method of the `OrderViewSet` in `views.py` to enable caching for the `/orders` endpoint.

    ```python
    from django.views.decorators.cache import cache_page
    from rest_framework import viewsets

    class OrderViewSet(viewsets.ModelViewSet):
        # ...
        @method_decorator(cache_page(60 * 15, key_prefix='order_list'))
            def list(self, request, *args, **kwargs):
                return super().list(request, *args, **kwargs)
    ```

4.  **Demonstrating the Problem:** After caching the response for user 2, a subsequent request is made with user 1's token. The lesson shows that the cached response for user 2 is incorrectly returned to user 1 because the cache key is only based on the URL `/orders`.

5.  **Applying `@vary_on_headers`:** The `@vary_on_headers('Authorization')` decorator is added to the `list` method of the `OrderViewSet`, along with `@cache_page`.

    ```python
    from django.views.decorators.cache import cache_page
    from rest_framework.decorators import vary_on_headers
    from rest_framework import viewsets

    class OrderViewSet(viewsets.ReadOnlyModelViewSet):
        # ...
        @method_decorator(cache_page(60 * 15, key_prefix='order_list'))
        @method_decorator(vary_on_headers('Authorization'))
        def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)
    ```

6.  **Flushing the Redis Cache:** The Redis cache is flushed to ensure a clean state for testing. This involves using Docker commands to access the Redis container and execute the `flushdb` command.

    ```bash
    docker ps

    # Find the Redis container ID
    docker exec -it <redis_container_id> bash
    ```

    ```bash
    redis-cli -n 1
    flushdb
    exit
    exit
    ```

7.  **Testing with `@vary_on_headers`:**
    - A request is sent as user 2. The correct orders for user 2 are returned and cached, with the cache key now taking the `Authorization` header into account.
    - A subsequent request is sent as user 1. The correct orders for user 1 are returned. This time, the cached response for user 2 is not used because the `Authorization` header is different. A new cached response is created for user 1.

This demonstrates that the `@vary_on_headers('Authorization')` decorator ensures that the cache distinguishes between different authenticated users based on their JWT tokens in the `Authorization` header, thus providing the correct user-specific cached responses.
