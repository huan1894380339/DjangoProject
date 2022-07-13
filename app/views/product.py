from __future__ import annotations

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app.models import Category, Product
from app.serializers.product import (
    CsvSerializer,
    ProductSerializer, ImgSerializer,
)
from app.tasks import upload_image_task
from app.utils import get_list_path_images
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg import openapi

from drf_yasg.utils import swagger_auto_schema


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'import_product_csv':
            return CsvSerializer
        if self.action == 'img_product_from_path':
            return ImgSerializer
        return ProductSerializer

    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        security=['None'],
        responses={
            201: 'Create account successfully',
            400: 'Invalid Information, Please check it again',

        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        security=['None'],
        manual_parameters=[
            openapi.Parameter(
                name='file',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
            ),
        ],
        responses={200: 'Create list product from csv successfully'},
    )
    @action(detail=False, methods=['post'])
    def import_product_csv(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(request.data)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def img_product_from_path(self, request: Request) -> Response:
        path = request.data['path']
        link_local = get_list_path_images(path)
        upload_image_task.delay(link_local)
        return Response(status=status.HTTP_200_OK)

    test_param = openapi.Parameter(
        'category', openapi.IN_QUERY, description='Category (Name)', type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(
        manual_parameters=[test_param],
        security=['None'],
        responses={
            200: ProductSerializer(many=True),

        },
    )
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
