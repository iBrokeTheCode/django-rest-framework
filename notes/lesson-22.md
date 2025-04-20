# Viewset Permissions: Admin vs. Normal User in Django REST Framework

## 1. Core Concepts:

- **Initial Authentication:** Initially, the `OrderViewSet` in this lesson uses the `IsAuthenticated` permission class, meaning that any user must be logged in to access any of the endpoints defined by the viewset. However, this initial setup allows all authenticated users to see all orders, which is often undesirable.
- **Problem of Overly Broad Access:** Allowing every authenticated user to view all orders in the database can lead to privacy and data security issues. Users typically should only have access to their own data.
- **Targeted Permission Rules:** The goal of this lesson is to implement more granular permissions:
  - Normal users should only be able to **view their own orders**.
  - Administrators should be able to **view all orders**.
  - Normal users should only be able to **update and delete their own orders**.
  - Administrators should be able to **update and delete all orders**.
- **Overriding `get_queryset`:** To achieve these targeted permissions, the lesson demonstrates overriding the **`get_queryset`** method within the `OrderViewSet`. This method controls which objects are returned by the viewset when fetching data.
- **Checking User's Staff Status:** The `get_queryset` method accesses the currently authenticated user via `self.request.user`. It then checks the **`is_staff`** property of the user object. In Django's user model, `is_staff` is a boolean field that indicates whether a user has administrator privileges and access to the Django admin.
- **Conditional Queryset Filtering:** Based on the user's `is_staff` status, the `get_queryset` method conditionally filters the base queryset. If the user is **not a staff member** (a normal user), the queryset is filtered to include only the `Order` objects that are associated with the authenticated user (`self.request.user`).
- **Default Behavior for Administrators:** If the user **is a staff member** (an administrator), the `get_queryset` method returns the original, unfiltered queryset, granting them access to all `Order` objects.
- **Application Across Viewset Actions:** The modification to the `get_queryset` method applies to **all actions** within the viewset, including list and detail views, as well as update and delete operations. This ensures consistent permission enforcement across all endpoints managed by the `OrderViewSet`.
- **Redundancy of Custom Actions:** By implementing this filtering in `get_queryset`, the need for custom actions to retrieve a user's specific orders becomes **redundant**. The default `/orders` endpoint will now automatically return only the requesting user's orders if they are not an administrator.
- **Leveraging Built-in Viewset Features:** Viewsets in Django REST Framework inherently provide a full set of URLs for CRUD operations, handle serialization/deserialization through serializers, and can be further enhanced with permission classes, pagination, and filtering. The `get_queryset` method allows for fine-grained control over the data accessible through these built-in features.
- **Extensibility through Method Overriding:** Django REST Framework's viewsets and generic views are designed to be extensible. Developers can override various methods to customize functionality, including permissions and object access.

## 2. Practical Steps:

1.  **Define the `get_queryset` method within your ViewSet:**
    Within your `OrderViewSet` class (or any viewset you want to apply this logic to), define the `get_queryset` method.

    ```python
    from rest_framework import viewsets
    from rest_framework.permissions import IsAuthenticated
    from .models import Order
    from .serializers import OrderSerializer

    class OrderViewSet(viewsets.ModelViewSet):
        serializer_class = OrderSerializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            queryset = super().get_queryset()
            # Further filtering logic will be added here
            return queryset
    ```

2.  **Get the base queryset using `super()`:**
    Inside the `get_queryset` method, retrieve the default queryset for the model associated with the viewset using `super().get_queryset()`. This fetches all orders from the database initially.

    ```python
    def get_queryset(self):
        queryset = super().get_queryset()
        # ...
        return queryset
    ```

3.  **Check if the requesting user is a staff member:**
    Access the currently authenticated user via `self.request.user` and check their `is_staff` attribute. This determines if the user is an administrator.

    ```python
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            # Filter for normal users
            pass
        return queryset
    ```

4.  **Filter the queryset for normal users:**
    If the user is not a staff member (`not self.request.user.is_staff` evaluates to `True`), filter the `queryset` to include only the orders belonging to the authenticated user. Assuming your `Order` model has a foreign key field named `user` that links it to the user who placed the order, you can filter as follows:

    ```python
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
    ```

5.  **Return the (potentially filtered) queryset:**
    The `get_queryset` method must return the `queryset`. This will be the set of `Order` objects that the viewset will operate on for the current request.

    ```python
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
    ```

6.  **Testing the implementation (using a tool like VS Code REST Client):**
    - **Obtain access tokens:** Use an endpoint to retrieve authentication tokens for both an administrator user (with `is_staff=True`) and a normal user (with `is_staff=False`).
    - **Send a GET request to the `/orders` endpoint with the administrator's token:** You should receive a list of **all orders** in the database.
    - **Send a GET request to the `/orders` endpoint with the normal user's token:** You should receive a list containing **only the orders associated with that specific user**.
    - **Attempt to access a specific order (e.g., `/orders/1/`) belonging to another user with the normal user's token:** This should result in a **404 Not Found** error because the `get_queryset` method will have filtered out that order for the non-admin user. This ensures that normal users cannot even view the details of orders created by others.
    - **Attempt to update or delete an order belonging to another user with the normal user's token:** These actions should also be restricted due to the filtered queryset, likely resulting in a "not found" error when the system tries to retrieve the specific object based on the filtered queryset.

By following these steps, you can effectively implement role-based data access control in your Django REST Framework viewsets, enhancing the security and privacy of your application.
