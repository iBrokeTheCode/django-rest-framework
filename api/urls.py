from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('products/info/', views.products_info),
    path('orders/', views.order_list),
    path('order-items/', views.order_item_list),
]
