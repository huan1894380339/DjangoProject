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
        membership = Membership.objects.select_related('user').filter(
            user=instance.user.id,
        ).first()
        return '%s%s' % (int(membership.voucher*100), '%')


class OrderDetailSerializer(serializers.ModelSerializer):
    cartitems = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'user', 'shiping_address', 'phone', 'created_at',
            'cartitems', 'cart_total',
        ]

    def get_cartitems(self, obj: Order):
        queryset = obj.cart_item.all()
        return CartItemSerializer(queryset, many=True).data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_status(self, status):
        order = self.instance
        if order.status not in ['NE', 'CO']:
            raise serializers.ValidationError(
                'Your order has been delivered to the shipping unit, Cannot cancel',
            )
        if status in ['CO', 'RE', 'SH']:
            raise serializers.ValidationError('Your do not permission')
        return status

    def validate_phone(self, phone):
        order = self.instance
        if order.status not in ['NE']:
            raise serializers.ValidationError(
                'Just edit when order status is New',
            )
        return phone

    def validate_shiping_address(self, shiping_address):
        order = self.instance
        if order.status not in ['NE']:
            raise serializers.ValidationError(
                'Just edit when status Order is New',
            )
        return shiping_address

    def validate_order_decription(self, order_decription):
        order = self.instance
        if order.status not in ['NE']:
            raise serializers.ValidationError(
                'Just edit when status Order is New',
            )
        return order_decription


class OrderAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def save(self):
        order = Order(
            user=self.context['user'],
            shiping_address=self.data['shiping_address'],
            order_decription=self.data['order_decription'],
            phone=self.data['phone'],
        )
        order.save()
        order.cart_item.add(*self.data['cart_item'])
