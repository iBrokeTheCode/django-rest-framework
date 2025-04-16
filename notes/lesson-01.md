# Django REST Framework Series - Setup and Models

## 1. Core Concepts

- **Django REST Framework:** This lesson introduces **Django REST Framework** as the key tool for building APIs in Django. It's highlighted as the most popular package for this task in the modern web development world.
- **API Development Focus:** The series will concentrate on building an API to manage **products and orders**, demonstrating common API functionalities.
- **CRUD Operations:** The API will showcase all the **CRUD (Create, Read, Update, Delete)** operations that can be performed on products, as well as viewing and listing products and individual product details over the API.
- **Key REST Framework Concepts (To be covered in the series):** While this lesson focuses on models, the video briefly mentions important concepts that will be explored in later videos. These include:
  - **Request and Response objects**
  - Different **views** and **generic views**
  - **Viewsets**
  - **Serializers** (to be covered in the next video, a core concept for converting between models and JSON)
  - **Validators**
  - **Authentication and Permissions** (covering different authentication scenarios)
  - **Caching and Throttling**
  - **Filtering and Pagination**
  - **Testing**
- **Data Models:** This specific lesson focuses on defining the core data models for the API:
  - **Product:** Represents individual products with attributes like name, description, price, stock, and an optional image.
  - **Order:** Represents customer orders and includes an order ID, association with a user, creation timestamp, and status (pending, confirmed, cancelled).
  - **OrderItem:** Acts as a **junction table** establishing a **many-to-many relationship** between Product and Order. It also stores additional information specific to the order, such as the quantity of a product in that particular order.
  - **User:** A custom user model extending Django's `AbstractUser` is set up, although no custom fields are added in this initial stage.
- **Relationships between Models:** The lesson explains the relationships:
  - A **Product** can be part of **multiple Orders**, and an **Order** can contain **multiple Products** (many-to-many relationship managed through `OrderItem`).
  - An **Order** is associated with one **User** through a **foreign key** relationship.
- **API-Focused Development:** The video emphasizes that the series will concentrate on building the API itself, and no client-side technologies like React or Vue.js will be used in this series. Interaction with the API will be demonstrated using tools like the REST client in VS Code.

## 2. Practical Steps

Here's a step-by-step guide to applying the concepts covered in this lesson:

1.  **Clone the Starter Code:**

    Clone the starter code for the series from the GitHub [repository](https://github.com/bugbytes-io/drf-course-api).

2.  **Create a Python Virtual Environment:**

    Create an isolated environment for the project dependencies.

    ```bash
    python -m venv venv-drf
    ```

3.  **Activate the Virtual Environment:**

    Activate the newly created virtual environment.

    ```bash
    # Linux and macOS
    source venv-drf/bin/activate

    # Windows
    .\venv-drf\Scripts\activate
    ```

4.  **Install Requirements:**

    Install the necessary packages listed in the `requirements.txt` file, including Django, Django REST Framework, Django Extensions, and Pillow.

    ```bash
    pip install -r requirements.txt
    ```

5.  **Define the Custom User Model (`api/models.py`):**

    - Action: Extend Django's `AbstractUser` to create a custom user model.
    - Code:

      ```python
      from django.contrib.auth.models import AbstractUser
      from django.db import models

      class User(AbstractUser):
          pass
      ```

6.  **Define the Product Model (`api/models.py`):**

    - Action: Create the `Product` model with its fields and the `in_stock` property and `__str__` method.
    - Code:

      ```python
      class Product(models.Model):
          name = models.CharField(max_length=200)
          description = models.TextField()
          price = models.DecimalField(max_digits=10, decimal_places=2)
          stock = models.PositiveIntegerField()
          image = models.ImageField(upload_to='products/', blank=True, null=True)

          @property
          def in_stock(self):
              return self.stock > 0

          def __str__(self):
              return self.name
      ```

7.  **Define the Order Model (`api/models.py`):**

    - Action: Create the `Order` model with its status choices, fields (including a UUID as the primary key), and the `__str__` method.
    - Code:

      ```python
      import uuid
      from django.conf import settings

      class Order(models.Model):
          class StatusChoices(models.TextChoices):
              PENDING = 'pending', 'Pending'
              CONFIRMED = 'confirmed', 'Confirmed'
              CANCELLED = 'cancelled', 'Cancelled'

          order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
          user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
          created_at = models.DateTimeField(auto_now_add=True)
          status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
          products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')

          def __str__(self):
              return f"Order {self.order_id} for {self.user}"
      ```

8.  **Define the OrderItem Model (`api/models.py`):**

    - Action: Create the `OrderItem` model as the through model for the many-to-many relationship between Order and Product, including the `quantity` field and the `item_subtotal` property and `__str__` method.
    - Code:

      ```python
      class OrderItem(models.Model):
          order = models.ForeignKey(Order, on_delete=models.CASCADE)
          product = models.ForeignKey(Product, on_delete=models.CASCADE)
          quantity = models.PositiveIntegerField()

          @property
          def item_subtotal(self):
              return self.product.price * self.quantity

          def __str__(self):
              return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"
      ```

9.  **Register the Custom User Model in `settings.py`:**

    - Action: Tell Django to use the custom user model defined in the `api` application.
    - Code (`settings.py`):
      ```python
      AUTH_USER_MODEL = 'api.User'
      ```

10. **Create Migrations:**

    - Action: Generate the migration files based on the newly defined models.
    - Code:
      ```bash
      python manage.py makemigrations
      ```

11. **Apply Migrations:**

    - Action: Apply the migrations to create the corresponding tables in the database.
    - Code:
      ```bash
      python manage.py migrate
      ```

12. **Populate the Database:**
    - Action: Run the custom management command (`populatedb`) provided in the starter code to add initial user, product, and order data to the database.
    - Code:
      ```bash
      python manage.py populatedb
      ```

## 3. Resources

- The lesson mentions the **Django REST Framework documentation** as a valuable resource. (A direct link was not provided in the video).
- A link to the **GitHub repository for the course** containing the starter code is available in the video description. (A direct link was not provided in the video).
- The video references a previous video on the **`graph_models` command** from Django Extensions. (A direct link was not provided in the video).
- The **Graphviz online website** used to generate the entity-relationship diagram is mentioned. (A direct link was not provided in the video).
