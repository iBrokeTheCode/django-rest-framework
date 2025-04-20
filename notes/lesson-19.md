# API Pagination in Django REST Framework

## 1. Key Concepts

Django REST Framework provides built-in pagination classes to handle the process of dividing API responses into pages. This lesson focuses on two main types of pagination:

- **PageNumberPagination:** This method uses a **page number** in the request query parameters to determine which page of data to return. The API response includes links to the **next** and **previous** pages, as well as a **count** of the total number of records. The actual data for the current page is typically found within a **results** key in the JSON response.

- **LimitOffsetPagination:** This approach mirrors the SQL `LIMIT` and `OFFSET` clauses. The request URL includes a **limit** parameter, specifying the number of records to retrieve, and an **offset** parameter, indicating where to start fetching records from.

Both pagination methods can be configured globally in the `settings.py` file or on a per-view basis in the `views.py` file. This allows for customization of the default page size and the specific pagination style used for different API endpoints. Additionally, clients can sometimes be allowed to control the page size within certain limits.

## 2. Resources

- [Django REST Framework Pagination](https://www.django-rest-framework.org/api-guide/pagination/)
- [PageNumberPagination](https://www.django-rest-framework.org/api-guide/pagination/#pagenumberpagination)
- [LimitOffsetPagination](https://www.django-rest-framework.org/api-guide/pagination/#limitoffsetpagination)

## 3. Practical Steps

This section provides a step-by-step guide on how to implement and customize pagination in Django REST Framework, based on the lesson.

**Setting up default PageNumberPagination globally:**

1.  Open your project's `settings.py` file.
2.  Locate the `REST_FRAMEWORK` dictionary. If it doesn't exist, create it.
3.  Add the `DEFAULT_PAGINATION_CLASS` and `PAGE_SIZE` settings within this dictionary. For example, to use `PageNumberPagination` with a default page size of 5, add the following:

    ```python
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 5
    }
    ```

    This will apply `PageNumberPagination` to all API endpoints that return a list of data by default. The `PAGE_SIZE` determines the number of items included on each page.

**Overriding pagination settings on a per-view basis:**

1.  In your `views.py` file, import the desired pagination class:

    ```python
    from rest_framework.pagination import PageNumberPagination
    ```

2.  For a specific API view (e.g., a `ListAPIView` or a `ViewSet`), add the `pagination_class` attribute and optionally the `page_size` attribute directly to the view class:

    ```python
    from rest_framework import generics
    from .models import Product
    from .serializers import ProductSerializer
    from rest_framework.pagination import PageNumberPagination

    class ProductListCreateAPIView(generics.ListCreateAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        pagination_class = PageNumberPagination
        page_size = 2  # Override the default page size for this view
    ```

    Here, `PageNumberPagination` is explicitly set for this view, and the `page_size` is set to 2, overriding the global setting.

**Handling the unordered object list warning:**

1.  When using pagination, especially `PageNumberPagination`, with an unordered queryset, Django REST Framework might issue a warning about inconsistent results.
2.  To resolve this, ensure that your queryset has a defined ordering. You can achieve this in your view by adding an `order_by()` clause to your queryset:

    ```python
    class ProductListCreateAPIView(generics.ListCreateAPIView):
        queryset = Product.objects.all().order_by('pk') # Order by primary key
        serializer_class = ProductSerializer
        pagination_class = PageNumberPagination
        page_size = 2
    ```

    Ordering by a stable field like the primary key ensures consistent pagination.

**Customizing the page query parameter name:**

1.  To change the name of the query parameter used for the page number (default is `page`), you can modify the `page_query_param` attribute of the pagination class.
2.  This can be done globally by creating a custom pagination class and setting it as the `DEFAULT_PAGINATION_CLASS` in `settings.py`, or on a per-view basis by setting it in the view:

    ```python
    from rest_framework.pagination import PageNumberPagination

    class CustomPageNumberPagination(PageNumberPagination):
        page_query_param = 'pageNum'

    class ProductListCreateAPIView(generics.ListCreateAPIView):
        queryset = Product.objects.all().order_by('pk')
        serializer_class = ProductSerializer
        pagination_class = CustomPageNumberPagination # Use the custom pagination class
        page_size = 2
    ```

    Now, the page number will be specified using `pageNum` in the URL (e.g., `/products/?pageNum=2`).

**Allowing client-side control of page size:**

1.  To let clients specify the number of items per page, you can add the `page_size_query_param` attribute to your pagination class.
2.  You can also set a `max_page_size` to prevent clients from requesting excessively large pages.

    ```python
    from rest_framework.pagination import PageNumberPagination

    class CustomPageNumberPagination(PageNumberPagination):
        page_query_param = 'pageNum'
        page_size_query_param = 'size'  # Allow clients to set page size with 'size' parameter
        max_page_size = 4          # Limit the maximum page size
    ```

    Clients can now use the `size` query parameter (e.g., `/products/?size=3`) to request a specific number of items per page, up to the `max_page_size`.

**Implementing LimitOffsetPagination:**

1.  In your `views.py` file, import the `LimitOffsetPagination` class:

    ```python
    from rest_framework.pagination import LimitOffsetPagination
    ```

2.  Set the `pagination_class` of your view to `LimitOffsetPagination`:

    ```python
    from rest_framework import generics
    from .models import Product
    from .serializers import ProductSerializer
    from rest_framework.pagination import LimitOffsetPagination

    class ProductListAPIView(generics.ListAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        pagination_class = LimitOffsetPagination
        # page_size = 2 # Default limit if not overridden in settings
    ```

    The default `limit` will be determined by the global `PAGE_SIZE` setting if not overridden here.

3.  Clients can then use the `limit` and `offset` query parameters to retrieve specific sets of records (e.g., `/products/?limit=4&offset=6`). The `limit` specifies the number of records to return, and the `offset` specifies the starting position.

**Customizing LimitOffsetPagination:**

1.  `LimitOffsetPagination` also allows customization of the query parameter names for `limit` and `offset` using the `limit_query_param` and `offset_query_param` attributes, respectively.
2.  You can also set a `max_limit` to restrict the maximum number of records a client can request.

    ```python
    from rest_framework.pagination import LimitOffsetPagination

    class CustomLimitOffsetPagination(LimitOffsetPagination):
        default_limit = 10
        limit_query_param = 'max_results'
        offset_query_param = 'start_from'
        max_limit = 100

    class ProductListAPIView(generics.ListAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        pagination_class = CustomLimitOffsetPagination
    ```

    In this example, the default limit is set to 10, the limit query parameter is changed to `max_results`, the offset parameter is changed to `start_from`, and the maximum limit is set to 100.
