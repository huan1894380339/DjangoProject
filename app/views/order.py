from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from uritemplate import partial
from app.models import Order
from app.serializers.pagination import DefaultPagination
from app.serializers.order import OrderDetailSerializer, OrderAddSerializer
from app.authentication import IsTokenValid
from app.serializers.order import OrderSerializer
from rest_framework.decorators import action
from rest_framework import status


class OrderViewSet(ModelViewSet):
    permission_classes = [IsTokenValid]
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'all_order_by_user':
            return OrderDetailSerializer
        if self.action == 'create':
            return OrderAddSerializer
        return OrderSerializer

    def retrieve(self, request, pk=None):
        order = Order.objects.select_related('user').filter(
            id=pk,
        ).first()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(
            data=request.data, context={'user': request.user},
        )
        serializer.is_valid()
        serializer.save()
        return Response({'message': 'success'})

    def partial_update(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(
            order, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsTokenValid])
    def all_order_by_user(self, request):
        queryset = Order.objects.select_related(
            'user',
        ).filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
