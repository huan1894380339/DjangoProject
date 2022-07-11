from __future__ import annotations

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app.models import Category, Product
from app.serializers.product import (
    CsvSerializer,
    ProductSerializer,
)
from app.tasks import upload_image_task
from app.utils import get_list_path_images
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'import_product_csv':
            return CsvSerializer
        return ProductSerializer

    def create(self, request, *args, **kwargs):
        import ipdb;ipdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'])
    def import_product_csv(self, request):
        serializer_class = self.get_serializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.create(request.data)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def img_product_from_path(self, request: Request) -> Response:
        path = request.data['path']
        link_local = get_list_path_images(path)
        upload_image_task.delay(link_local)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def list_product_by_category(self, request):
        category = Category.objects.get(
            title=request.query_params.get('category'),
        )
        queryset = Product.objects.filter(
            category=category,
        ).order_by('-id')[:10]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def new_product(self, request):
        queryset = Product.objects.all().order_by('-id')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def list_new_product_by_category(self, request):
        category = Category.objects.get(
            title=request.query_params.get('category'),
        )
        queryset = Product.objects.filter(
            category=category,
        ).order_by('-id')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
