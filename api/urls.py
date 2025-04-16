from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.list_products, name='list_products')
]
