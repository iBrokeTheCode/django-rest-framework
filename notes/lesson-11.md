# Django REST Framework - Customizing Permissions in Generic Views

## 1. Key Concepts

- The lesson highlights the need to **customize permissions** for API views that perform multiple roles, such as retrieving a list of resources (GET request) and creating a new resource (POST request).
- The default approach of setting the `permission_classes` attribute on a generic view applies the same permissions to all types of requests, which is insufficient for scenarios requiring different access controls for different actions.
- Django REST Framework provides several methods for customizing access restrictions:
  - Overriding the `get_queryset` method, which limits the visibility of existing objects.
  - Using the `permission_classes` attribute for general permission checks.
  - Overriding the **`get_permissions` method**, which allows for dynamic permission setting based on the current action or request. This is the primary focus of the lesson.
- Overriding `get_permissions` enables you to **dynamically alter the permissions** applied based on the type of request (e.g., GET, POST) by inspecting the `self.request.method`.
- The lesson demonstrates using the `AllowAny` permission class, which grants access to any user, and the `IsAdminUser` permission class, which restricts access to Django administrator users.
- By default, the lesson sets `self.permission_classes` to `AllowAny` within the `get_permissions` method, allowing unrestricted access. Then, it uses a conditional statement to change the `permission_classes` to `IsAdminUser` specifically for POST requests.
- The **REST Client extension for VS Code** is introduced as a tool to send HTTP requests and view responses directly within the editor, streamlining the API testing process without the need for external applications like Postman or Insomnia. This involves creating files with the `.http` extension to define API requests.

## 2. Resources

- [DRF Access Restriction Methods](https://www.django-rest-framework.org/api-guide/permissions/#overview-of-access-restriction-methods)
- [VSCode REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)
- [curl cheat sheet](./curl-cheatsheet.md)

## 3. Practical Steps

To configure a global default permission, you can add the following code in your `settings.py` file.

```py
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}
```

1.  **Identify the API view requiring different permissions for different request methods.**
    In this lesson, the target is the `ProductListCreateAPIView`. It should allow anyone to retrieve the list of products (GET request) but restrict the creation of new products (POST request) to admin users only.

2.  **Import the necessary permission classes** from `rest_framework.permissions`.

    ```python
    from rest_framework.permissions import AllowAny, IsAdminUser
    ```

    These permission classes will be used to define the access rules.

3.  **Override the `get_permissions` method** within your generic view class.
    This method is called by the Django REST Framework to determine which permissions should be applied to the current request.

    ```python
    def get_permissions(self):
        # ... permission logic here ...
        return super().get_permissions()
    ```

4.  **Set a default permission class.**
    Initially, set `self.permission_classes` to `[AllowAny]` to permit GET requests from any user. If the request method is `'POST'`, change `self.permission_classes` to `[IsAdminUser]` to enforce admin-level access for creating new products.

    ```python
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    ```

5.  **Test the API endpoints using the REST Client extension in VS Code.**

    - Additionally, can do the same task with `curl`. Review [commands](./curl-cheatsheet.md)
    - Create a file (e.g., `api.http`) with the `.http` extension.
    - Define a GET request to the product list endpoint.
      ```http
      GET http://127.0.0.1/products/ HTTP/1.1
      ```
    - Define a POST request to the same endpoint to create a new product, including the `Content-Type` header and a JSON body. Separate requests with `###`.

      ```http
      ###

      POST http://your-api-endpoint/products/ HTTP/1.1
      Content-Type: application/json

      {
          "name": "Test Product",
          "price": 300.00,
          "stock": 14,
          "description": "An amazing new TV"
      }
      ```

    - With `curl`

      ```shell
      # GET request
      curl -i http://127.0.0.1:8000/products/

      # POST request
      curl -X POST -i http://127.0.0.1:8000/products/ \
      -H 'Content-Type: application/json' \
      -u user:password \
      -d '{
            "name": "Test Product",
            "price": 300.00,
            "stock": 14,
            "description": "An amazing new TV"
        }'
      ```

    - Sending the GET request should return the list of products without any authentication required.
    - Sending the POST request without proper admin authentication should result in a **403 Forbidden** response, indicating that the permission restriction is working. The response detail will likely state that "Authentication credentials were not provided".

    ```

    ```

This approach of overriding `get_permissions` allows for fine-grained control over API access based on the specific actions being performed on an endpoint. The subsequent video will delve into integrating JWT (JSON Web Token) authentication to securely handle user roles and permissions.
