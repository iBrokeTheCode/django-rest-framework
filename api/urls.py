from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:pk>/', views.product_detail),
    path('products/info/', views.products_info),
    path('orders/', views.order_list),
    path('order-items/', views.order_item_list),
]
