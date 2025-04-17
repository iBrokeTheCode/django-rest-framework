from django.contrib import admin
from django.urls import path, include

from api.views import product_list, product_detail, order_list, order_item_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('orders/', order_list, name='order_list'),
    path('order-items/', order_item_list, name='order_item_list'),
    # path('api-auth/', include('rest_framework.urls'))
]
