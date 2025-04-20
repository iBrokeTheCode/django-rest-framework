# Creating Nested Objects in Django REST Framework

## 1. Key Concepts

- **Writable Nested Representations**: This refers to the ability to create not only a primary object but also its related (nested) objects in a single API request, typically a POST request. For example, creating an order and simultaneously specifying the items that belong to that order.
- **Overriding the `create()` method**: When dealing with writable nested representations, the default `create()` method of a `ModelSerializer` is insufficient. To handle the creation of multiple related objects, you need to **override the `create()` method** in your serializer. This allows you to customize how the incoming data is processed and how the related objects are instantiated and saved.
- **Separate Serializers for Create Operations**: It's often beneficial to create **specific serializers for create (and sometimes update) operations** that might differ from the serializers used for retrieving data (GET requests). This provides flexibility in terms of the data expected in the request body and the data returned in the response.
- **`get_serializer_class()` in ViewSets**: Django REST Framework's `ViewSet` and generic views offer the `get_serializer_class()` method. By overriding this, you can **dynamically determine which serializer class to use** based on the current action (e.g., `create` for POST requests) or the request method. This allows you to use your dedicated create serializer for POST requests and a different serializer for other actions like listing or retrieving orders.
- **`perform_create()` in ModelViewSet**: The `ModelViewSet` provides the `perform_create()` method, which is called when saving a new object. You can **override this method to inject additional data** into the serializer's `save()` method, such as the currently authenticated user, without requiring the client to provide it in the request.
- **Read-only Nested Serializers for Retrieval**: For GET requests, nested serializers are often set to `read_only=True`. This allows related data to be included in the response when retrieving the main object without expecting this data in the request body for creation or updates.
- **Defining Nested Serializers**: Nested serializers are defined as fields within a parent serializer. To handle multiple related objects (like a list of order items), you use the `many=True` argument when declaring the nested serializer field. You can even define these nested serializers as **inner classes** within the parent serializer if they are not intended for use outside that specific context.

## 2. Resources

- [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Classy DRF](https://www.cdrf.co/)

## 3. Practical Steps

1.  **Identify the need for writable nested representations**: The initial `OrderSerializer` had a nested `OrderItemSerializer` with `read_only=True`, meaning order items could not be created when a new order was submitted via a POST request.

2.  **Attempt (and revert) making the nested serializer writable**: Initially, the `read_only=True` constraint was removed from the `OrderItemSerializer` within the `OrderSerializer`. However, this led to issues because the expected input format in the POST request did not match the serializer's structure, and HTML input did not support lists directly.

3.  **Create a dedicated serializer for order creation (`OrderCreateSerializer`)**:

    - A new serializer, `OrderCreateSerializer`, was created to specifically handle the creation of orders and their items.
    - **Define a nested serializer for creating order items (`OrderItemCreateSerializer`)**: An inner class `OrderItemCreateSerializer` was created within `OrderCreateSerializer` to define the fields required for creating individual order items (e.g., `product` ID and `quantity`).

      ```python
      class OrderCreateSerializer(serializers.ModelSerializer):
          class OrderItemCreateSerializer(serializers.ModelSerializer):
              class Meta:
                  model = OrderItem
                  fields = ('product', 'quantity')

          items = OrderItemCreateSerializer(many=True)

          class Meta:
              model = Order
              fields = ('user', 'status', 'items', 'total_price')
      ```

4.  **Override `get_serializer_class()` in the `OrderViewSet`**: This method was overridden to use the `OrderCreateSerializer` specifically for the `create` action (POST requests).

    ```python
    from .serializers import OrderSerializer, OrderCreateSerializer

    class OrderViewSet(viewsets.ModelViewSet):
        serializer_class = OrderSerializer
        # ... other configurations ...

        def get_serializer_class(self) -> type:
            # can also check if POST: if self.request.method == 'POST'
            if self.action == 'create':
                return OrderCreateSerializer
            return super().get_serializer_class()
    ```

5.  **Override the `create()` method in `OrderCreateSerializer`**: The `create()` method was overridden to handle the creation of both the `Order` and its associated `OrderItem`s.

    ```python
    class OrderCreateSerializer(serializers.ModelSerializer):
        class OrderItemCreateSerializer(serializers.ModelSerializer):
            class Meta:
                model = OrderItem
                fields = ('product', 'quantity')

        order_id = serializers.UUIDField(read_only=True)
        items = OrderItemCreateSerializer(many=True)

        def create(self, validated_data):
            order_item_data = validated_data.pop('items')
            order = Order.objects.create(**validated_data)

            for item in order_item_data:
                OrderItem.objects.create(order=order, **item)

            return order
    ```

    - The `items` data was popped from the `validated_data` dictionary.
    - The `Order` object was created using the remaining `validated_data`.
    - The code then iterated through the `order_item_data` and created each `OrderItem`, associating it with the newly created `Order`.
    - Finally, the created `Order` object was returned.
    - **Add `order_id` to the `OrderCreateSerializer` response**: To include the `order_id` in the response after a successful POST request, a read-only `order_id` field was added to the `OrderCreateSerializer`.

6.  **Automatically set the user using `perform_create()`**: To avoid requiring the client to send the `user_id` in the POST request, the `perform_create()` method was overridden in the `OrderViewSet` to automatically set the `user` based on the authenticated user making the request.

    ```python
    class OrderViewSet(viewsets.ModelViewSet):
        serializer_class = OrderSerializer
        # ... other configurations ...

        def get_serializer_class(self):
            if self.action == 'create':
                return OrderCreateSerializer
            return super().get_serializer_class()

        # Overwrite this method
        def perform_create(self, serializer):
            serializer.save(user=self.request.user)
    ```

7.  **Make the `user` field read-only in `OrderCreateSerializer`**: After implementing `perform_create()` to auto-set the user, the `user` field in `OrderCreateSerializer` was made read-only using the `extra_kwargs` in the `Meta` class. This prevents the client from specifying the user during order creation.

    ```python
    class OrderCreateSerializer(serializers.ModelSerializer):
        order_id = serializers.UUIDField(read_only=True)
        items = OrderItemCreateSerializer(many=True)
        # ... other fields ...

        class Meta:
            model = Order
            fields = ['order_id', 'user', 'status', 'items']
            extra_kwargs = {'user': {'read_only': True}}
    ```

By following these steps and overriding the `create()` method, the lesson demonstrates how to effectively handle the creation of nested objects in Django REST Framework, providing a more flexible and efficient API for clients.
