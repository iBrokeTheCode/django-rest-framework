from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
    path('products/create/', views.ProductCreateAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('orders/', views.OrderListAPIView.as_view()),
    path('user-orders/', views.UserOrderListAPIView.as_view(), name='user_orders'),
    path('order-items/', views.OrderItemListAPIView.as_view()),
]
