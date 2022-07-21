
from rest_framework.generics import CreateAPIView
from app.models import Discount
from app.serializers.discount import DiscountSerializer
from rest_framework.pagination import PageNumberPagination


class DiscountViewSet(CreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    pagination_class = PageNumberPagination
