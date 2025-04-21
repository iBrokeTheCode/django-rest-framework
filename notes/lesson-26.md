# Caching with Redis and Django!

## 1. Key Concepts

- **Caching** is a crucial method for enhancing API performance and reducing the load on databases and servers. This involves storing frequently accessed data in a faster storage medium (like in-memory) to avoid repeated computations or database queries.
- The lesson focuses on caching **data that doesn't commonly change** and caching at **busy API endpoints**.
- **Redis** is introduced as a very fast **in-memory data platform** that is well-suited for caching. It functions as a **key-value database** and also supports vector search and NoSQL capabilities. While it primarily stores data in memory, it also offers persistence options.
- To use Redis with a Python application, the **`redis-py`** Python client is necessary. The lesson recommends installing the high-performance version using `pip install redis[hiredis]`.
- **Django's cache framework** natively supports Redis. You can configure it in the `CACHES` setting of your `settings.py` file.
- The lesson utilizes **`django-redis`**, a more fully featured cache backend for Django, offering advanced features beyond Django's built-in Redis cache.
- The **`@cache_page` decorator** from Django is used to cache the output of an individual view. When applied to a view, it stores the entire HTTP response in the cache for a specified duration.
- For class-based views and viewset methods, the **`@method_decorator`** is required in conjunction with `@cache_page`.
- The `cache_page` decorator caches responses based on the **specific URL**, meaning different query parameters or pagination settings will result in separate cache entries.
- **Cache invalidation** is essential to ensure that the cached data remains relatively accurate when the underlying data is modified.
- **Django signals** (`post_save`, `post_delete`) can be used to trigger cache invalidation when changes occur to models. A **receiver function** connected to these signals can perform actions like clearing the cache.
- The **`delete_pattern` function** provided by `django-redis` allows for the removal of all cache keys matching a given pattern, which is useful for invalidating multiple related cache entries based on a key prefix. This function uses wildcard operators to match keys.
- It's important to consider what data is suitable for caching. **Data that changes frequently is not a good candidate** for caching, as it would require complex invalidation strategies. Relatively static data or data where a slight delay in updates is acceptable are ideal for caching.

## 2. Resources

- [Redis DockerHub](https://hub.docker.com/_/redis)
- [DRF Caching](https://www.django-rest-framework.org/api-guide/caching/)
- [django-redis](https://github.com/jazzband/django-redis)
- [Django Signals - Introduction!](https://youtu.be/8p4M-7VXhAU?si=abr9ABQ0868ZYTGm)

## 3. Practical Steps

1.  **Set up a Redis cache using Docker:**
    To start a Redis instance using Docker, execute the following command in your terminal. This command will:

    - Run a container in detached mode (`-d`).
    - Name the container `Django-Redis` (`--name Django-Redis`).
    - Expose port `6379` from the host to the container (`-p 6379:6379`).
    - Automatically remove the container when it is stopped (`--rm`).
    - Use the `redis` image.

    ```bash
    docker run -d --name Django-Redis -p 6379:6379 --rm redis
    ```

    This sets up a Redis instance accessible on `localhost:6379`.

2.  **Install the `redis-py` and `django-redis` packages:**
    Install the necessary Python libraries in your virtual environment using pip. The `redis[hiredis]` package includes a faster parser for improved performance.

    ```bash
    pip install "redis[hiredis]"
    pip install django-redis
    ```

3.  **Configure Django to use Redis for caching:**
    In your Django project's `settings.py` file, add or modify the `CACHES` setting to configure the default cache to use `django-redis`. You can specify the location (Redis URL), database number, and client class.

    ```python
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
    ```

    Here, `"redis://127.0.0.1:6379/1"` indicates that we are connecting to Redis on localhost, port 6379, and using database number 1 (Redis provides multiple databases).

4.  **Cache an API view's list method using `@cache_page`:**
    To cache the response of an API view's list method, import the necessary decorators from Django and Django REST Framework. Then, use `@method_decorator(cache_page(...))` above the `list` method within your viewset or generic view.

    ```python
    from django.utils.decorators import method_decorator
    from django.views.decorators.cache import cache_page
    from rest_framework import generics

    class ProductListCreateAPIView(generics.ListCreateAPIView):
        queryset = Product.objects.order_by('pk')
        serializer_class = ProductSerializer
        filterset_class = ProductFilter
        filter_backends = (
            DjangoFilterBackend,
            filters.SearchFilter,
            filters.OrderingFilter,
            InStockFilter
        )
        search_fields = ('name', 'description')
        ordering_fields = ('name', 'price', 'stock')
        pagination_class = CustomPagination

        @method_decorator(cache_page(60 * 15, key_prefix='product_list'))
        def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)

        def get_permissions(self):
            self.permission_classes = (AllowAny,)
            if self.request.method == 'POST':
                self.permission_classes = (IsAdminUser,)
            return super().get_permissions()
    ```

    The `cache_page` decorator takes the cache timeout in seconds (here, 15 minutes) and an optional `key_prefix`. The `key_prefix` helps in identifying and invalidating related cache entries later.

5.  **(Optional) Simulate database latency for demonstration:**
    To easily observe the effect of caching, you can temporarily add a delay in the `get_queryset` method of your view. This simulates a slow database query.

    ```python
    import time
    from rest_framework import generics

    class ProductListCreateAPIView(generics.ListCreateAPIView):
        # ...
        def get_queryset(self):
            import time
            time.sleep(2)
            return super().get_queryset()
        # ...
    ```

    With this, the first request will take 2 seconds, but subsequent requests for the same URL will be served from the cache immediately.

6.  **Implement cache invalidation using Django signals:**

    a. **Create a `signals.py` file** within your Django app directory and define a receiver function for the `post_save` and `post_delete` signals of the model you want to track for cache invalidation (e.g., `Product`).

    ```python
    from django.db.models.signals import post_save, post_delete
    from django.dispatch import receiver
    from django.core.cache import cache
    from api.models import Product

    @receiver([post_save, post_delete], sender=Product)
    def invalidate_product_cache(sender, instance, **kwargs):
        print("Clearing the product cache")
        cache.delete_pattern("*product_list*")
    ```

    This function, `invalidate_product_cache`, will be called after a `Product` instance is saved or deleted. It uses `cache.delete_pattern("*product_list*")` to remove all cache entries with the `product_list` prefix, effectively invalidating the cached product list.

    b. **Register the signals** in your app's `apps.py` file within the `ready` method.

    ```python
    from django.apps import AppConfig

    class YourAppNameConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'your_app_name'

        def ready(self):
            import your_app_name.signals
    ```

    Replace `your_app_name` with the actual name of your Django application.

7.  **Observe cache behavior and invalidation:**
    After implementing caching and invalidation, test your API endpoints. The first request to a cached URL should be slower (if you added the `time.sleep`), but subsequent requests with the same URL should be much faster due to the cache. When you create, update, or delete `Product` objects (e.g., through the Django admin), the cache should be invalidated, and the next request to the product list endpoint should again take longer as it fetches fresh data from the database and re-caches the response.

8.  **(For development/testing) Verify cached content in Redis:**
    You can inspect the Redis database to see the cached entries.
    - First, get the ID of your running Redis container:
      ```bash
      docker ps
      ```
    - Then, access the Redis container's shell:
      ```bash
      docker exec -it <container_id> bash
      ```
    - Connect to the Redis client and select the database you configured in `settings.py` (in this case, database 1):
      ```bash
      redis-cli -n 1
      ```
    - List all keys related to your cached data (using the key prefix):
      ```bash
      KEYS *product_list*
      ```
    - Retrieve the value of a specific key:
      ```bash
      GET <key_from_previous_command>
      ```
      Remember that using `KEYS *` in production is generally discouraged as it can block the Redis server. This is primarily for development and debugging purposes. You will observe that the cached values are string representations of the API responses, often in HTML format due to the browsable API or JSON if the request specifies `format=json`.
