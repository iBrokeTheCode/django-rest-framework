# API Throttling with Django REST Framework

## 1. Core Concepts

- **Throttling Limits:** API throttling involves setting limits on the number of requests a client can make within a defined time frame (e.g., per minute, per hour, per day). If these limits are exceeded, the API will temporarily prevent further requests.
- **Global vs. Per-View Throttling:** Throttling policies can be set **globally** for the entire API or **on a per-view or per-view set basis** for more granular control.
- **Throttle Classes:** Django REST Framework provides different throttle classes:
  - **`AnonRateThrottle`**: Limits the rate of API calls for **anonymous users**.
  - **`UserRateThrottle`**: Limits the rate of API calls for **authenticated users**, using the user ID to track requests.
  - **`ScopedRateThrottle`**: Restricts access to **specific parts of the API** based on a defined scope within the view.
- **Throttle Rates:** These define the actual limits (e.g., number of requests per time period) associated with throttle classes and scopes.
- **HTTP Response:** When a request is throttled, the API typically returns a **429 Too Many Requests** status code. It may also include a **`Retry-After` header** indicating how many seconds the client should wait before making another request.
- **Custom Throttle Policies:** You can create **subclasses** of existing throttle classes (like `UserRateThrottle`) to implement more flexible policies, such as allowing a burst of requests within a short period and a sustained rate over a longer period.
- **Client Identification:** Django REST Framework identifies clients for throttling using headers like `HTTP_X_FORWARDED_FOR` and the `REMOTE_ADDR` WSGI variable to determine the client IP address.
- **Caching Backend:** Throttling in Django REST Framework utilizes Django's **cache backend** to track request counts for each user or anonymous client.
- **Not a Security Measure:** Application-level throttling in Django REST Framework is **not a primary security measure** against brute-force or denial-of-service (DoS) attacks. Malicious actors can spoof IP origins. It's intended for implementing business logic and basic protection against service overuse. More robust security measures like Web Application Firewalls (WAFs) and DoS protection services are recommended for stronger protection.

## 2. Resources

- [Throttling](https://www.django-rest-framework.org/api-guide/throttling/)

## 3. Practical Steps

**Step 1: Set global throttling policies.**

You can define global throttling policies in your project's `settings.py` file within the `REST_FRAMEWORK` setting. This involves specifying `DEFAULT_THROTTLE_CLASSES` and `DEFAULT_THROTTLE_RATES`.

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '2/minute',
        'user': '3/minute'
    }
}
```

This configuration, as demonstrated in the lesson, limits anonymous users to **two requests per minute** and authenticated users to **three requests per minute** across the entire API. The keys `'anon'` and `'user'` in `DEFAULT_THROTTLE_RATES` correspond to the throttle classes listed in `DEFAULT_THROTTLE_CLASSES`.

**Step 2: Implement custom throttle subclasses.**

To create more complex throttling policies (e.g., a burst rate and a sustained rate), create a new file (e.g., `throttles.py`) in your API application and define subclasses of `UserRateThrottle` (or `AnonRateThrottle`). Define a `scope` attribute for each subclass.

```python
# In api/throttles.py
from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
```

Then, update your `settings.py` to use these custom throttle classes and define their rates based on their `scope` attributes.

```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'api.throttles.BurstRateThrottle',
        'api.throttles.SustainedRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'burst': '10/minute',
        'sustained': '15/hour'
    }
}
```

This example from the lesson sets a limit of **10 requests per minute** (burst) and **15 requests per hour** (sustained) for authenticated users.

**Step 3: Use `ScopedRateThrottle` for specific API sections.**

To apply different throttling rates to different views, you can use the `ScopedRateThrottle`. First, add it to the `DEFAULT_THROTTLE_CLASSES` in `settings.py`.

```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'products': '2/minute',
        'orders': '4/minute'
    }
}
```

Next, in your `views.py`, for the specific API views or viewsets you want to apply scoped throttling to, add a `throttle_scope` attribute. The value of this attribute should match a key defined in `DEFAULT_THROTTLE_RATES`.

```python
# In views.py
from rest_framework import generics, viewsets
from rest_framework.throttling import ScopedRateThrottle
# ... your other imports

class ProductListCreateAPIView(generics.ListCreateAPIView):
    # ... your other configurations
    throttle_scope = 'products'

class OrderViewSet(viewsets.ModelViewSet):
    # ... your other configurations
    throttle_scope = 'orders'
```

Now, requests to `/products` will be limited to **two per minute**, and requests to `/orders` will be limited to **four per minute**. As shown in the lesson, different endpoints with the same `throttle_scope` will share the same rate limit.

**Step 4: Set throttling on a per-view basis.**

You can override the global throttling settings for a specific view by defining a `throttle_classes` attribute directly within the view class in your `views.py`. This allows you to apply specific throttle classes (including `ScopedRateThrottle` or custom ones) to individual views, regardless of the global settings.

```python
# In views.py
from rest_framework import generics
from rest_framework.throttling import ScopedRateThrottle, AnonRateThrottle
# ... your other imports

class ProductListCreateAPIView(generics.ListCreateAPIView):
    # ... your other configurations
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'products'

class SomeOtherView(generics.RetrieveUpdateDestroyAPIView):
    # ... your other configurations
    throttle_classes = [AnonRateThrottle]
```

In this example, `ProductListCreateAPIView` will only use the `ScopedRateThrottle` defined by its `throttle_scope`, and `SomeOtherView` will only use the `AnonRateThrottle`, irrespective of the global `DEFAULT_THROTTLE_CLASSES`.
