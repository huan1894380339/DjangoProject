from rest_framework import serializers
from app.models import CartItem, CustomerUser, Order, Product, Membership
from app.models import Discount
from django.utils import timezone


class ItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title')
    category = serializers.CharField(source='product.category.title')
    cart_id = serializers.IntegerField(source='id')
    price = serializers.FloatField(source='product.price')
    voucher = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'cart_id',
            'quantity',
            'title',
            'category',
            'price',
            'item_total',
            'voucher',
            'item_total_after_apply_voucher',
        ]

    def get_voucher(self, request):
        membership = Membership.objects.select_related('user').filter(
            user=request.user.id,
        ).first()
        return '%s%s' % (membership.voucher, '%')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            discount = Discount.objects.get(product=instance.product)
            if timezone.now() < discount.day_end:
                price_discount = instance.product.price - \
                    instance.product.price * discount.value_discount
                representation['price'] = {
                    'original_price': instance.product.price,
                    'discount_price': price_discount, 'discount_value': f'{int(discount.value_discount*100)}%',
                }
        except Exception:
            representation['price'] = instance.product.price

        return representation


class CartItemSerializer(serializers.Serializer):
    total = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()

    def get_item(self, request):
        queryset = CartItem.objects.filter(user=request.user, status='W')
        return ItemSerializer(queryset, many=True).data

    def get_total(self, request):
        cartitem = CartItem.objects.filter(user=request.user, status='W')
        total = sum(
            product.item_total_after_apply_voucher()
            for product in cartitem
        )
        return total


class CartItemForAddOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def save(self):
        order = Order.objects.get(id=self.context['order'])
        user = CustomerUser.objects.get(id=self.data['user'])
        product = Product.objects.get(id=self.data['product'])
        cartitem = CartItem(
            user=user,
            product=product,
            quantity=self.data['quantity'],
            order=order,
        )
        cartitem.save()
