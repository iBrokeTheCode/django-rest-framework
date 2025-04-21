# Celery Tasks with Django REST Framework

**Introduction**

## 1. Core Concepts

- **Distributed Task Queue**: Celery is described as a **distributed system** used to process large volumes of messages. It functions as a **task queue**, which is a mechanism to distribute work across threads or machines.
- **Tasks**: The input to a task queue is a **unit of work** called a task. In this lesson, the task is sending an order confirmation email.
- **Worker Processes**: Dedicated **worker processes** constantly monitor the task queue for new tasks to perform. The Celery worker is the process that executes the defined tasks in the background.
- **Broker**: Celery communicates via **messages**, and it uses a **broker** to mediate between clients (the Django application) and workers. Common brokers include **Redis**, RabbitMQ, and Amazon SQS. This lesson utilizes **Redis** as the broker.
- **Asynchronous Processing**: The core idea behind using Celery in this context is to perform tasks **asynchronously** in the background. When a task is triggered, it is added to the queue, and a worker picks it up and processes it independently of the main application flow. This prevents the client from having to wait for the task to complete.
- **Task Scheduling (Celery Beat)**: While the main focus of this lesson is immediate background task execution, it is mentioned that Celery also supports **task scheduling** using a component called **Celery Beat**. This allows for tasks to be run at specific times or intervals, a topic intended for a future series.
- **`delay()` method**: The `.delay()` method is a convenient way to schedule a Celery task to be executed asynchronously. It sends the task with its arguments to the broker.
- **`@shared_task` decorator**: This decorator from the `celery` library is used to define Celery task functions in Django applications.

## 2. Resources

- [Celery](https://github.com/celery/celery)
- [Celery Docs](https://docs.celeryq.dev/en/stable/)
- [Celery and Django](https://docs.celeryq.dev/en/stable/django/index.html)

## 3. Practical Steps

1.  **Install Celery**:
    To begin, Celery needs to be installed using pip.

    ```
    pip install celery
    ```

2.  **Set up Celery in the Django project**:
    Create a file named `celery.py` within your Django project directory. This file will contain the Django-specific setup for Celery.

3.  **Define the Celery app**:
    In the `celery.py` file, import necessary modules and create a Celery application instance. Configure it to use Django settings and enable task discovery.

    ```python
    import os
    from celery import Celery

    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_course.settings')

    app = Celery('drf_course')

    # read config from Django settings, the namespace='CELERY' means
    # all celery config keys should have a `CELERY_` prefix.
    app.config_from_object('django.conf:settings', namespace='CELERY')

    # autodiscover tasks in all registered Django app configs.
    app.autodiscover_tasks()

    # @app.task(bind=True)
    # def debug_task(self):
    #     print(f'Request: {self.request!r}')
    ```

    The `os.environ.setdefault` line sets the Django settings module for Celery. The `Celery('drf_course')` line creates the Celery application with the project name. `app.config_from_object('django.conf:settings', namespace='CELERY')` tells Celery to read its configuration from the Django `settings.py` file, looking for variables prefixed with `CELERY_`. `app.autodiscover_tasks()` automatically finds Celery tasks defined in `tasks.py` files within your Django applications.

4.  **Ensure Celery app loading**:
    In your project's `__init__.py` file, import the Celery app instance to ensure it's loaded when Django starts.

    ```python
    from .celery import app as celery_app

    __all__ = ('celery_app',)
    ```

    This step ensures that the Celery application is initialized early in the Django startup process, making the `@shared_task` decorator available.

5.  **Configure Celery settings**:
    In your Django `settings.py` file, define the `CELERY_BROKER_URL` to specify the message broker. In this lesson, Redis is used. Optionally, you can also define a `CELERY_RESULT_BACKEND` to store task results and configure the `EMAIL_BACKEND` for testing.

    ```python
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    ```

    The `CELERY_BROKER_URL` tells Celery how to connect to the Redis broker. The `EMAIL_BACKEND` is set to `django.core.mail.backends.console.EmailBackend` to print emails to the terminal instead of sending real emails.

6.  **Define Celery tasks**:
    Within a Django application (e.g., `api`), create a file named `tasks.py`. Define your Celery tasks in this file using the `@shared_task` decorator. This lesson demonstrates a task to send an order confirmation email.

    ```python
    from celery import shared_task
    from django.core.mail import send_mail
    from django.conf import settings

    @shared_task
    def send_order_confirmation_email(order_id, user_email):
        subject = 'Order Confirmation'
        message = f'Your order with ID {order_id} has been received and is being processed.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]
        return send_mail(subject, message, from_email, recipient_list)
    ```

    The `@shared_task` decorator registers the `send_order_confirmation_email` function as a Celery task. The function takes the `order_id` and `user_email` as arguments and uses Django's `send_mail` function to send the email.

7.  **Schedule the Celery task**:
    In your Django view (e.g., the `perform_create` method of an `OrderViewSet`), after performing the action that should trigger the background task (like saving a new order), import the Celery task and call its `.delay()` method with the required arguments.

    ```python
    from rest_framework import viewsets
    from .models import Order
    from .serializers import OrderSerializer
    from api.tasks import send_order_confirmation_email # Assuming tasks.py is in the 'api' app

    class OrderViewSet(viewsets.ModelViewSet):
        queryset = Order.objects.all()
        serializer_class = OrderSerializer

        def perform_create(self, serializer):
            order = serializer.save(user=self.request.user)
            send_order_confirmation_email.delay(order.order_id, self.request.user.email)
    ```

    After a new order is created and saved, `send_order_confirmation_email.delay(order.order_id, self.request.user.email)` schedules the Celery task to be executed asynchronously with the provided order ID and user email.

8.  **Run the Django development server**:
    Start your Django development server as usual.

    ```shell
    python manage.py runserver
    ```

9.  **Start the Celery worker**:
    Open a new terminal and navigate to your project directory. Run the Celery worker process, specifying the application name (`drf_course`) and the log level.

    ```shell
    celery -A drf_course worker -loglevel=INFO
    ```

    This command starts the Celery worker, which connects to the Redis broker and waits for tasks to be added to the queue.

10. **Test the integration**:
    Make a request to your Django REST Framework endpoint that triggers the creation of an order (e.g., a POST request to an `/orders/` endpoint). You should receive a response quickly from Django as the email sending task has been offloaded to Celery. In the Celery worker terminal, you should see output indicating that the `send_order_confirmation_email` task was received and executed, and the email content should be printed to the console due to the configured `EMAIL_BACKEND`.
