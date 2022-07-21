from rest_framework.viewsets import ModelViewSet
from app.serializers.cartitem import ItemSerializer
from app.models import CartItem
from app.authentication import IsTokenValid
from rest_framework.pagination import PageNumberPagination


class CartItemViewset(ModelViewSet):
    permission_classes = [IsTokenValid]
    serializer_class = ItemSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        try:
            queryset = CartItem.objects.filter(
                user=self.request.user, status='W',
            )
        except Exception:
            queryset = []
        return queryset
