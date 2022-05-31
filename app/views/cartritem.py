from rest_framework.viewsets import ModelViewSet
from app.serializers.cartitem import CartItemSerializer
from app.models import CartItem
from rest_framework.permissions import IsAuthenticated


class CartItemViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
