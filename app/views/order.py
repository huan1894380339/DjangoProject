from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app.models import Order
from app.serializers.pagination import DefaultPagination
from app.serializers.order import OrderDetailSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from app.authentication import IsTokenValid


class ManageOrder(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    pagination_class = DefaultPagination

    def retrieve(self, request, pk=None):
        order = Order.objects.filter(
            id=pk,
        ).prefetch_related('orderitem').first()
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)


class GetAllOrderByUser(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsTokenValid]

    def list(self, request):
        queryset = Order.objects.filter(user=request.data['user'])
        serializer = OrderDetailSerializer(queryset, many=True)
        return Response(serializer.data)
