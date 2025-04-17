from django.shortcuts import get_object_or_404
from django.db.models import Max, Min

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics


from api.models import Product, Order, OrderItem
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductsInfoSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'


@api_view(['GET'])
def order_list(request):
    orders = Order.objects.prefetch_related('items__product')
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def order_item_list(request):
    order_items = OrderItem.objects.all()
    serializer = OrderItemSerializer(order_items, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def products_info(request):
    products = Product.objects.all()

    serializer = ProductsInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price'],
        'min_price': products.aggregate(min_price=Min('price'))['min_price']
    })

    return Response(serializer.data)
