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
