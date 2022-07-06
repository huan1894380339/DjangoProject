from rest_framework.viewsets import ModelViewSet
from app.serializers.cartitem import ItemSerializer
from app.models import CartItem
from app.authentication import IsTokenValid


class CartItemViewset(ModelViewSet):
    permission_classes = [IsTokenValid]
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = CartItem.objects.filter(user=self.request.user, status='W')
        return queryset
