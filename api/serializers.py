from rest_framework import serializers

from api.models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'stock')

    def validate_price(self, value: float) -> float:
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')

        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ('product_name', 'product_price', 'quantity', 'item_subtotal')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    def get_total_price(self, order) -> float:
        return sum(item.item_subtotal for item in order.items.all())

    class Meta:
        model = Order
        fields = ('order_id', 'user', 'created_at',
                  'status', 'items', 'total_price')


class ProductsInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
    min_price = serializers.FloatField()
