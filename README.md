# Django REST Framework Tutorial

## Credits

> [!NOTE]
> Material by [BugBytes Channel](https://www.youtube.com/@bugbytes3923) and [tutorial series](https://www.youtube.com/watch?v=6AEvlNgRPNc&list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t).
> Notes generated with [NotebookLM](https://notebooklm.google)

**Prompt**

```txt
Generate a README file (Markdown format) summarizing the key concepts of the source video. Include the following sections:

Introduction: A brief overview of the video's topic. (don't add numeration for this section)
1. Core Concepts: Explain the main functionalities and principles discussed.
2. Practical Steps: Provide a step-by-step guide for the practical application of the concepts in the video. For each step, clearly explain the action and include the corresponding code block (if any) directly after the step description. (not required to put "action" or "code" subtitle)

Refer to the source as "lesson", for example: "In this lesson ..."
```

## Table of Contents

1. [Django REST Framework series - Setup and Models](./notes/lesson-01.md) | [Tutorial](https://youtu.be/6AEvlNgRPNc?si=YBnUAiGHIXL3mndx)

   In this initial lesson, the primary focus is on setting up the project and defining the fundamental data models for an API centered around **products and orders**.

2. [Django REST Framework - Serializers & Response objects | Browsable API](./notes/lesson-02.md) | [Tutorial](https://youtu.be/BMym71Dwox0?si=OBaDKuWnOaug7b8r)

   This lesson introduces **serializers**, highlighting their importance for converting complex Django data types (like querysets and model instances) into Python primitives that can be rendered into formats like JSON. It also covers the inverse process of deserialization. Additionally, introduces the **Browsable API** and the **Response object** provided by Django REST Framework.

3. [Django REST Framework- Nested Serializers, SerializerMethodField and Serializer Relations](./notes/lesson-03.md) | [Tutorial](https://youtu.be/KfSYadIFHgY?si=IlS4-iodg5ZRKQtL)

   In this lesson, we delve into techniques for serializing complex data structures involving related models in Django REST Framework. We will learn how to represent one-to-many relationships by embedding serialized data of related models within the parent object's representation. Additionally, we will explore how to add custom, read-only fields to our API responses using `SerializerMethodField` and examine different ways to represent foreign key relationships.

4. [Django REST Framework - Serializer subclasses and Aggregated API data](./notes/lesson-04.md) | [Tutorial](https://youtu.be/_xbI0-mjtw4?si=wXfWJNA5QxNbh72c)

   This lesson provides an overview of how to create generic serializers in Django REST Framework that are not tied to specific models. It demonstrates how to aggregate data from different sources (in this case, a database) and return it as a single JSON response to clients.

5. [django-silk for Profiling and Optimization with Django REST Framework](./notes/lesson-05.md) | [Tutorial](https://youtu.be/OG8alXR4bEs?si=zMjLTCjqt-fH4Oig)

   This lesson focuses on using the **Django Silk** package to profile and optimize Django REST Framework APIs, with a particular emphasis on optimizing database queries for better performance. The lesson demonstrates how to install and configure Django Silk, use it to inspect HTTP requests and their associated SQL queries, and identify and resolve database query performance issues like the N+1 problem using Django's `prefetch_related` feature.

6. [Django REST Framework - Generic Views | ListAPIView & RetrieveAPIView](./notes/lesson-06.md) | [Tutorial](https://youtu.be/vExjSChWPWg?si=fdIM8l1yAK_Fmtii)

   In this lesson, we explore the power of class-based generic views in DRF. Generic views in DRF offer a streamlined approach to building common API endpoints by abstracting common idioms and patterns in view development. This lesson focuses on read-only generic views, specifically `ListAPIView` and `RetrieveAPIView`, demonstrating how they simplify the process of creating API views that closely map to database models for common CRUD operations.

7. [Django REST Framework - Dynamic Filtering | Overriding get_queryset() method](./notes/lesson-07.md) | [Tutorial](https://youtu.be/3Gi-w4Swge8?si=arj4kv2XprfTKHae)

   In this lesson, we will explore how to dynamically filter data returned by Django REST Framework generic API views, specifically focusing on overriding the `get_queryset()` method. This technique allows you to customize the set of objects retrieved from the database based on dynamic information, such as the currently authenticated user.

8. [Django REST Framework - Permissions and Testing Permissions](./notes/lesson-08.md) | [Tutorial](https://youtu.be/rx5IV_4Iuog?si=WjcKg4NyyEMW4_aZ)

   This lesson introduces **permissions in Django REST Framework** and demonstrates how to create and apply them to generic view classes. It addresses the issue of unauthorized access to user-specific data and explains how permissions, in conjunction with authentication, control access to API endpoints. The lesson also covers how to write tests to ensure that permissions are enforced correctly.

9. [Django REST Framework - APIView class](./notes/lesson-09.md) | [Tutorial](https://youtu.be/TVFCU0w65Ak?si=cp5gKS3_aph13EGH)

   This lesson introduces the **APIView class** in Django REST Framework and demonstrates how to extend it to create API views in your Django application. It shows how to replace a function-based view with an `APIView`-based class view.

10. [Django REST Framework - Creating Data | ListCreateAPIView and Generic View Internals](./notes/lesson-10.md) | [Tutorial](https://youtu.be/Jh85U1nhMh8?si=Ea0hqVhwnC0oxbqe)

    In this lesson, we explore how to create data in a Django REST Framework application using generic views, specifically focusing on `CreateAPIView` and `ListCreateAPIView`. We'll also touch upon the underlying HTTP methods and the internal workings of these generic views.

11. [Django REST Framework - Customising permissions in Generic Views | VSCode REST Client extension](./notes/lesson-11.md) | [Tutorial](https://youtu.be/mlQZ1i8rUKQ?si=b4x-ObQXwoy8s3p1)

    This lesson explores how to customize permissions in Django REST Framework generic views on a case-by-case basis. It addresses scenarios where different permissions are required for different operations (e.g., GET vs. POST requests) on the same API endpoint. The lesson focuses on overriding the `get_permissions` method to dynamically apply permission classes based on the type of request. It also introduces the REST Client extension for VS Code as a convenient tool for testing APIs.

12. [Django REST Framework - JWT Authentication with djangorestframework-simplejwt](./notes/lesson-12.md) | [Tutorial](https://youtu.be/Xp0-Yy5ow5k?si=RcZpSf6nlEnVsVY5)

    In this lesson, we explore how to add **JSON Web Token (JWT) authentication** to a Django REST Framework (DRF) API using the `djangorestframework-simplejwt` package. This method allows clients to authenticate by sending a token in an HTTP header, which the API can then verify to permit or deny access to specific endpoints.

13. [Django REST Framework - Updating & Deleting data](./notes/lesson-13.md) | [Tutorial](https://youtu.be/08gHVFPFuBU?si=QZ0BjKxkzRATd8qr)

    This lesson explains how to implement update and delete functionality in a Django REST Framework API using generic views. It focuses on utilizing pre-built classes provided by the framework to streamline the process of building API endpoints for modifying single model instances.
