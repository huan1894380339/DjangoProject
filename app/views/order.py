from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app.models import Order
from app.serializers.pagination import DefaultPagination
from app.serializers.order import OrderDetailSerializer
from app.authentication import IsTokenValid
from app.serializers.cartitem import CartItemForAddOrderSerializer
from app.serializers.order import OrderSerializer
from rest_framework.decorators import action


class OrderViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    pagination_class = DefaultPagination

    def retrieve(self, request, pk=None):
        order = Order.objects.filter(
            id=pk,
        ).prefetch_related('orderitem').first()
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)

    def create(self, request):
        import ipdb
        ipdb.set_trace()
        serializer = OrderSerializer(data=request.data['order'])
        serializer.is_valid()
        serializer.save()
        order_id = serializer.data['id']
        for item in request.data['cartitems']:
            serializer = CartItemForAddOrderSerializer(
                data=item, context={'order': order_id},
            )
            serializer.is_valid()
            serializer.save()
        return Response({'message': 'success'})

    @action(detail=False, methods=['get'], permission_classes=[IsTokenValid])
    def all_order_by_user(self, request):
        queryset = Order.objects.filter(user=request.user)
        serializer = OrderDetailSerializer(queryset, many=True)
        return Response(serializer.data)
