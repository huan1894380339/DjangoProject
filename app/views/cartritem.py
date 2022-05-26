from rest_framework.viewsets import ModelViewSet
from app.serializers.cartitem import CartItemSerializer
from app.models import CartItem


class CartItemViewset(ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
