from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', views.product_list),
    path('products/<int:pk>/', views.product_detail),
    path('products/info/', views.products_info),
    path('orders/', views.order_list),
    path('order-items/', views.order_item_list),
    # path('api-auth/', include('rest_framework.urls'))
]
