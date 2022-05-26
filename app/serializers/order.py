from rest_framework import serializers

from app.models import CartItem, Order, Membership


class CartItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title')
    cart_id = serializers.IntegerField(source='id')
    price = serializers.FloatField(source='product.price')
    voucher = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'cart_id',
            'quantity',
            'title',
            'price',
            'item_total',
            'voucher',
            'item_total_after_apply_voucher',
        ]

    def get_voucher(self, instance):
        membership = Membership.objects.get(customeruser=instance.user.id)
        return '%s%s' % (membership.voucher, '%')


class OrderDetailSerializer(serializers.ModelSerializer):
    cartitems = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['user', 'cartitems', 'cart_total']

    def get_cartitems(self, obj: Order):
        queryset = obj.orderitem.all().select_related('product')
        return CartItemSerializer(queryset, context={'user': obj.user}, many=True).data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        field = '__all__'
