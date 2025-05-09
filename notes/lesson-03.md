# Django REST Framework - Nested Serializers, SerializerMethodField and Serializer Relations

## 1. Core Concepts

- **API View Decorator:** The `@api_view` decorator wraps function-based views, ensuring that the request object passed to the view is an instance of the Django REST Framework's `Request` object, not the standard Django `HttpRequest`. These decorated views are also allowed to return Django REST Framework's `Response` object.

- **Model Serializers:** To easily serialize data from Django models, you can inherit from `serializers.ModelSerializer`. By defining an inner `Meta` class, you can specify the `model` the serializer is associated with and the `fields` from that model that should be included in the serialized output.

- **Nested Serializers:** To represent related data within a serializer, you can declare a field as an instance of another serializer. For one-to-many relationships, use `many=True` when instantiating the nested serializer field. The `read_only=True` argument can be used to specify that these nested objects are returned on read requests (e.g., GET) but are not required for creating or updating the parent object (e.g., POST, PUT).

- **Related Name:** For Django's ORM to automatically fetch related objects in nested serializers, the foreign key field in the related model should have a `related_name` attribute that matches the field name in the parent serializer that holds the nested serializer. For example, if an `Order` model has a related set of `OrderItem` models through a foreign key named `order` on `OrderItem`, setting `related_name='items'` on the `order` field in `OrderItem` allows the `OrderSerializer` to automatically access the order items if it has a field named `items` using the `OrderItemSerializer`. You can then access these related items via `order.items.all()`.

- **SerializerMethodField:** This is a read-only field whose value is obtained by calling a method on the serializer class it's attached to. By default, the method name is `get_<field_name>`, where `<field_name>` is the name of the `SerializerMethodField`. The method should accept the instance of the object being serialized as a parameter (conventionally named `obj`). This is useful for adding calculated or aggregated values to the serialized output.

- **Serializer Relations (Representing Foreign Keys):** Django REST Framework provides various ways to represent model relationships:

  - **PrimaryKeyRelatedField (Default):** By default, foreign keys are represented by the primary key of the related object.
  - **Nested Serializers:** Instead of just the primary key, you can embed the serialized data of the related object by declaring a serializer instance as the foreign key field.
  - **StringRelatedField:** Represents the related object using its `__str__` method.
  - **HyperlinkedRelatedField:** Represents the related object using a hyperlink to its API endpoint. This requires defining a `view_name` that corresponds to the view for the related object.
  - **SlugRelatedField:** Represents the related object using a specific field (the 'slug') on the target model. You need to specify the `slug_field` in the `SlugRelatedField` definition.

- **Accessing Related Fields via `source`:** When you want to include specific fields from a related model at the same level as the parent object's fields (flattening the data), you can use a standard serializer field (e.g., `CharField`, `DecimalField`) and set its `source` attribute using dot notation to traverse the relationship. For example, if an `OrderItem` has a foreign key to `Product` with a `name` attribute, you can add a `product_name = serializers.CharField(source='product.name')` field to the `OrderItemSerializer`.

- **Referring to Model Properties:** If your Django model has defined properties (using the `@property` decorator), you can directly include them as fields in your `ModelSerializer`'s `fields` list, even though they don't correspond to database columns.

## 2. Resources

- [Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Serializer Relations](https://www.django-rest-framework.org/api-guide/relations/)
- [SerializerMethodField](https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield)

## 3. Practical Steps

**Step 1: Define Model Serializers.**

Create serializers for the models you want to serialize, inheriting from `serializers.ModelSerializer`. Define the `Meta` class to specify the `model` and the `fields` to include.

```python
# serializers.py
from rest_framework import serializers
from .models import Order, OrderItem, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock')

    def validate_price(self, value: float) -> float:
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')

        return value

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'quantity')
```

**Step 2: Implement Nested Serialization.**

In the parent serializer, add a field that is an instance of the related serializer, setting `many=True` for one-to-many relationships.

```python
# serializers.py
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('order_id', 'user', 'created_at',
                  'status', 'items')
```

If you don't add the related field (items in this case), by default DRF return only the `pk` and not the rest of item information.

**Step 3: Ensure `related_name` is Set in the Model.**

In the related model's foreign key field, ensure the `related_name` attribute matches the field name used for the nested serializer in the parent.

```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items') # set related_name here
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.quantity * self.product.price

    def __str__(self) -> str:
        return f'{self.quantity} x {self.product.price} in Order {self.order.order_id}'
```

**Step 4: Create a View to Return Serialized Data.**

Use a function-based view decorated with `@api_view` to fetch data and serialize it using the defined serializer.

```python
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)
```

**Step 5: Define URLs for the View.**

Map the view to a URL endpoint in your `urls.py`.

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
]
```

**Step 6: Implement `SerializerMethodField`.**

Add a `serializers.SerializerMethodField()` to your serializer and define the corresponding `get_<field_name>` method.

```python
# serializers.py
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField() # By default looks for "get_<field_name>"
    # total_price = serializers.SerializerMethodField(method_name='get_total_price') # Explicitly

    def get_total_price(self, order):
        return sum(item.item_subtotal for item in order.items.all())

    class Meta:
        model = Order
        fields = ('order_id', 'user', 'created_at',
                  'status', 'items', 'total_price')
```

**Step 7: Return Product details in Order serializer**

Add a nested serializer inside the `OrderItemSerializer`

```py
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')
```

**Step 8: Use `source` to Flatten Related Data.**

In a serializer, define a field and set its `source` attribute to access a field from a related model.

```python
# serializers.py
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ['quantity', 'product_name', 'product_price'] # Removed 'product' foreign key
```

**Step 9: Refer to Model Properties in Serializer Fields.**

Directly add the name of a model property to the `fields` list in your `ModelSerializer`.

```python
# serializers.py
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal' # It's a property of OrderItem (Can call you directly)
        )
```

These steps demonstrate the fundamental techniques for working with nested serializers, `SerializerMethodField`, and accessing related data in Django REST Framework.
