from django.urls import path

from rest_framework import routers

from api import views

app_name = 'api'

urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    # path('orders/', views.OrderListAPIView.as_view()),
    path('user-orders/', views.UserOrderListAPIView.as_view(), name='user_orders'),
    path('order-items/', views.OrderItemListAPIView.as_view()),
    path('users/', views.UserListAPIView.as_view())
]

router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet)

urlpatterns += router.urls
