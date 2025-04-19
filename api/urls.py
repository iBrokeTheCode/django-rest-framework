from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('orders/', views.OrderListAPIView.as_view()),
    path('user-orders/', views.UserOrderListAPIView.as_view(), name='user_orders'),
    path('order-items/', views.OrderItemListAPIView.as_view()),
]
