# API Documentation with drf-spectacular in Django REST Framework

## 1. Key Concepts

- **drf-spectacular** is an open API 3 schema generation library for Django REST Framework with a focus on extensibility, customizability, and client generation. It is a popular and well-regarded package in the Django community.
- The library helps in generating an **OpenAPI 3 schema** that describes your API's endpoints, request/response bodies, parameters, and other relevant details. This schema can then be used to generate interactive API documentation.
- Besides `drf-spectacular`, the lesson briefly mentions other options like Swagger generators for generating Swagger/OpenAPI 2 documentation, similar to what comes out of the box in frameworks like FastAPI and Django Ninja.
- `drf-spectacular` provides a way to serve the generated schema directly from your API and also offers user interfaces like **Swagger UI** and **Redoc UI** for a more user-friendly browsing experience of the API documentation.
- The generated documentation is **derived from your Django REST Framework serializers** and views, automatically including information about data types, request/response examples, and available HTTP methods for each endpoint.

## 2. Resources

- [Documenting DRF API](https://www.django-rest-framework.org/topics/documenting-your-api/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/readme.html)

## 3. Practical Steps:

**Step 1: Install drf-spectacular using pip.**

Open your terminal and run the following command within your project's virtual environment:

```bash
pip install drf-spectacular
```

**Step 2: Add `drf_spectacular` to your `INSTALLED_APPS` in `settings.py`.**

Open your project's `settings.py` file and add `'drf_spectacular'` to the `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    # ... other apps
    'drf_spectacular',
]
```

**Step 3: Set the default schema class in your REST framework settings in `settings.py`.**

Within the `REST_FRAMEWORK` setting in your `settings.py` file, add or modify the `DEFAULT_SCHEMA_CLASS` option:

```python
REST_FRAMEWORK = {
    # ... other settings
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

**Step 4: Optionally add `SPECTACULAR_SETTINGS` in `settings.py` for project metadata.**

You can configure metadata like the API title, description, and version by adding a `SPECTACULAR_SETTINGS` dictionary in your `settings.py` file:

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Description of your awesome API',
    'VERSION': '1.0.0',
    # ... other settings
}
```

**Step 5: Generate the `schema.yaml` file using the `spectacular` management command.**

```bash
python manage.py spectacular --color --file schema.yml
```

This command will generate a `schema.yaml` file in your project root (or as specified) containing the OpenAPI 3 schema of your API.

**Step 6: Include the URL patterns for serving the schema and the UI views in your project's `urls.py`.**

Open your project's `urls.py` file and add the following import and URL patterns:

```python
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # ... other URL patterns
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

These URL patterns will provide the following endpoints:

- `/api/schema/`: Downloads the `schema.yaml` file.
- `/api/schema/swagger-ui/`: Provides the interactive Swagger UI for your API documentation.
- `/api/schema/redoc/`: Provides the Redoc UI for your API documentation.

After following these steps and running your Django development server, you can access your API documentation through the `/api/schema/swagger-ui/` and `/api/schema/redoc/` endpoints in your browser. The schema can also be downloaded from the `/api/schema/` endpoint. This documentation will dynamically reflect your API structure based on your Django REST Framework views and serializers.
