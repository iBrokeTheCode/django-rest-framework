# Updating Nested Objects in Django REST Framework

## 1. Core Concepts

- In Django REST Framework, when dealing with nested objects, standard ModelSerializers handle creation automatically when you override the `create()` method. However, updating nested objects requires a different approach using the **`update()` method** on the serializer.

- The `update()` method differs from `create()` in its signature: it takes the **existing instance** of the model and the **validated data** from the request as arguments. This makes sense because an update operation inherently works on an already existing object.

- When a PUT request containing nested data is received, Django REST Framework needs instructions on how to handle these related objects. By overriding the `update()` method, you gain control over this process. This includes deciding how to handle situations where related data is present, absent, or needs to be modified. You might want to update existing related objects, create new ones, or even delete those that are no longer present in the request. The lesson demonstrates a simplified approach of clearing existing related objects and creating new ones based on the data in the PUT request.

- A crucial aspect of updating related data is considering **database integrity**. To prevent partial updates where the main object might be updated but the related objects aren't (or vice-versa), the lesson emphasizes wrapping the update logic within a **database transaction** using Django's `transaction.atomic`. This ensures that either all the changes are committed to the database, or if any part fails, the entire operation is rolled back.

- The lesson also briefly touches upon how Django REST Framework's **`ModelViewSet`** automatically handles **DELETE requests** through its `destroy` action, without requiring specific serializer method overrides.

## 2. Resources

- [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Classy DRF](https://www.cdrf.co/)

## 3. Practical Steps

1.  **Override the `update()` method in your serializer.** This method will handle the logic for updating the main object and its nested relations.

    ```python
    def update(self, instance, validated_data):
        pass
    ```

2.  **Extract the nested data from the `validated_data`.** Use the `pop()` method to remove the data for the nested objects (e.g., `items` for `OrderItem`) from the `validated_data`. This prevents the main model serializer from trying to handle the nested data directly.

    ```python
    items_data = validated_data.pop('items', None)
    ```

3.  **Update the main instance using the parent class's `update()` method.** Call `super().update(instance, validated_data)` to allow the default `ModelSerializer` update logic to handle the fields of the main object.

    ```python
    instance = super().update(instance, validated_data)
    ```

4.  **Handle the nested object updates.** Check if the nested data (`items_data` in this example) exists in the request. If it does, you can implement your desired update logic. The lesson demonstrates clearing existing related objects and creating new ones.

    ```python
    if items_data is not None:
        # Clear existing related items
        instance.items.all().delete()
        # Create new related items
        for item_data in items_data:
            OrderItem.objects.create(order=instance, **item_data)
    ```

5.  **Return the updated instance.** The `update()` method should return the updated model instance.

    ```python
    return instance
    ```

6.  **(Optional) Make nested fields optional during updates.** If you want to allow PUT requests without the nested data, you can set `required=False` in the nested serializer definition within your main serializer. This prevents validation errors when the nested data is missing.

    ```python
    class OrderCreateSerializer(serializers.ModelSerializer):
        items = OrderItemCreateSerializer(many=True, required=False)
        # ...
    ```

7.  **Wrap the update logic in a database transaction.** To ensure atomicity, use `transaction.atomic()` as a context manager around the code that updates the main object and its related objects.

    ```python
    from django.db import transaction

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if items_data is not None:
                instance.items.all().delete()
                for item_data in items_data:
                    OrderItem.objects.create(order=instance, **item_data)
            return instance
    ```

8.  **Configure the viewset to use the serializer with the `update()` method for PUT requests.** In your viewset's `get_serializer_class` method, specify the serializer containing the overridden `update()` method for the 'create' and 'update' actions.

    ```python
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return OrderCreateSerializer
        return OrderSerializer
    ```
