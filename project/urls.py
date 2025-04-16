from django.contrib import admin
from django.urls import path, include

from api.views import product_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('api.urls', namespace='api')),
    # path('api-auth/', include('rest_framework.urls'))
]
