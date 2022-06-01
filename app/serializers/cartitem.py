from rest_framework import serializers
from app.models import CartItem, CustomerUser, Order, Product


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartItemSerializerForAddOrder(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def save(self):
        order = Order.objects.filter(user=self.data['user']).last()
        user = CustomerUser.objects.get(id=self.data['user'])
        product = Product.objects.get(id=self.data['user'])
        cartitem = CartItem(
            user=user,
            product=product,
            quantity=self.data['quantity'],
            order=order,
        )
        cartitem.save()
