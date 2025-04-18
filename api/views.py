from django.db.models import Max, Min

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

from api.models import Product, Order, OrderItem
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductsInfoSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = (AllowAny,)
        if self.request.method == 'POST':
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = (AllowAny,)
        if self.request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class OrderItemListAPIView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()

        serializer = ProductsInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price'],
            'min_price': products.aggregate(min_price=Min('price'))['min_price']
        })

        return Response(serializer.data)
