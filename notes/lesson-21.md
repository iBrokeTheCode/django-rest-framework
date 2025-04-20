# Django REST Framework Viewsets: Actions, Filtering, and Permissions

## 1. Core Concepts:

- **Viewsets:** Viewsets in Django REST Framework provide a way to group related views into a single class. They inherit from `ModelViewSet`, offering built-in actions for CRUD (Create, Retrieve, Update, Destroy) operations.
- **Filtering:** Viewsets allow for easy data filtering using **filter backends**. The **`DjangoFilterBackend`** enables filtering based on fields defined in a **`FilterSet`** class.
  - A `FilterSet` class specifies which model fields can be filtered and the types of lookups allowed (e.g., exact match, case-insensitive contains, less than, greater than, range).
  - Custom filtering can be implemented by overriding filter fields in the `FilterSet`. For example, to filter orders by the date part of a `DateTimeField`, a `DateFilter` can be used with the `date` lookup modifier.
  - To enable filtering in a viewset, you need to set the **`filter_backends`** attribute to a list containing the desired backend (e.g., `[DjangoFilterBackend]`) and the **`filterset_class`** attribute to your custom `FilterSet`.
- **Custom Actions:** Viewsets can be extended with custom functionalities beyond the basic CRUD operations by defining extra actions.
  - The **`@action` decorator** from `rest_framework.decorators` is used to mark ad-hoc methods in a viewset as routable actions.
  - The `detail` argument in `@action` specifies whether the action applies to a single object (`detail=True`) or a collection (`detail=False`).
  - The `methods` argument in `@action` defines the HTTP methods allowed for the custom action (e.g., `['get']`, `['post']`).
  - The `url_path` argument in `@action` allows you to customize the URL segment for the action.
- **Permissions:** Django REST Framework provides a flexible way to manage permissions in viewsets.
  - **`permission_classes`** attribute can be set on a viewset to apply the specified permission classes to all actions within that viewset. For example, `permission_classes = [IsAuthenticated]` ensures that only authenticated users can access any action in the viewset.
  - Permissions can also be applied at the individual action level using the **`permission_classes`** argument within the `@action` decorator. This allows for different permission requirements for different custom actions.

## 2. Resources

- [Django REST Framework Viewsets](https://www.django-rest-framework.org/api-guide/viewsets/)
- [Classy DRF](https://www.cdrf.co/)
- [Django REST Framework Routers](https://www.django-rest-framework.org/api-guide/routers/)
- [isort formatter](https://pycqa.github.io/isort/)
- [Viewsets @action](https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing)

## 3. Practical Steps:

**Step 1: Define a FilterSet class.**

Create a file (e.g., `filters.py` in your API app) and define a `FilterSet` that inherits from `django_filters.FilterSet`. Specify the model and the fields you want to allow filtering on, along with the lookup types.

```python
# api/filters.py
import django_filters
from .models import Order

# Other filters
class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'status': ('exact',),
            'created_at': ('lt', 'gt', 'exact')
        }
```

**Step 2: Use the custom FilterSet in a ViewSet.**

In your viewset (e.g., `views.py` in your API app), import the `DjangoFilterBackend` and your custom `FilterSet`. Set the `filter_backends` and `filterset_class` attributes of your viewset.

```python
# api/views.py
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order
from .serializers import OrderSerializer
from .filters import OrderFilter

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter
```

**Step 3: Override Filter Fields for Advanced Filtering (e.g., date extraction).**

To filter based on the date part of a `DateTimeField`, override the field in your `FilterSet` with a `DateFilter` and use the `date` lookup modifier.

```python
# api/filters.py
import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')

    class Meta:
        model = Order
        fields = {
            'status': ('exact',),
            'created_at': ('lt', 'gt', 'exact')
        }
```

**Step 4: Define a custom action in a ViewSet.**

Use the `@action` decorator to create a new, routable method in your viewset.

```python
# api/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('order_items')
    serializer_class = OrderSerializer
    # ...

    @action(
        detail=False,
        methods=['get'],
        url_path='user-orders',
        permission_classes=[IsAuthenticated]
    )
    def user_orders(self, request):
        queryset = self.get_queryset().filter(user=request.user)  # orders
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

**Step 5: Register the ViewSet with the Router.**

Make sure your viewset is registered with the default router in your `urls.py` to automatically generate the URLs for the standard actions and any custom actions.

After these steps, you will have a viewset that supports filtering based on your defined criteria, includes a custom action accessible at the `/orders/user-orders/` endpoint (requiring authentication), and can have permissions applied at both the viewset and individual action levels.
