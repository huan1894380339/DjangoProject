from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from uritemplate import partial
from app.models import Order
from app.serializers.pagination import DefaultPagination
from app.serializers.order import OrderDetailSerializer, OrderAddSerializer
from app.authentication import IsTokenValid
from app.serializers.cartitem import CartItemForAddOrderSerializer
from app.serializers.order import OrderSerializer
from rest_framework.decorators import action
from rest_framework import status


class OrderViewSet(ModelViewSet):
    permission_classes = [IsTokenValid]
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    pagination_class = DefaultPagination

    def retrieve(self, request, pk=None):
        order = Order.objects.prefetch_related('orderitem').select_related('user').filter(
            id=pk,
        ).first()
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderAddSerializer(data=request.data['order'])
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

    def partial_update(self, request, pk=None):
        order = self.get_object()
        serializer = OrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = OrderSerializer(
            instance, data=request.data, partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsTokenValid])
    def all_order_by_user(self, request):
        queryset = Order.objects.filter(user=request.user)
        serializer = OrderDetailSerializer(queryset, many=True)
        return Response(serializer.data)
