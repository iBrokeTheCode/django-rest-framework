from django.http import JsonResponse

from .models import Product
from .serializers import ProductSerializer


def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)

    return JsonResponse(data={
        'data': serializer.data
    })
