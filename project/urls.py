from django.contrib import admin
from django.urls import path, include

from api.views import product_list, product_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail')
    # path('api-auth/', include('rest_framework.urls'))
]
