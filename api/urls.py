from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
    path('products/info/', views.products_info),
    path('orders/', views.OrderListAPIView.as_view()),
    path('user-orders/', views.UserOrderListAPIView.as_view()),
    path('order-items/', views.OrderItemListAPIView.as_view()),
]
