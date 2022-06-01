from __future__ import annotations

from pathlib import Path

from django.core.files import File
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app.models import Category, Product
from app.serializers.gallery import GallerySerializer
from app.serializers.product import (
    CsvSerializer, ImgSerializer,
    ProductSerializer,
)
from app.utils import get_list_path_images
from rest_framework.decorators import action


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == 'import_product_csv':
            return CsvSerializer
        return ProductSerializer

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
        for i in link_local.get('AnhChinh'):
            product = Product.objects.filter(title=str(Path(i).stem)).first()
            serializer = ImgSerializer(instance=product, data={'path': i})
            serializer.is_valid(raise_exception=True)
            print('111111111111')
            serializer.update(serializer.validated_data, product)
            print('222222222222')
        for i in link_local.get('AnhPhu'):
            product = Product.objects.filter(
                title=str(Path(i).stem).split('_')[0],
            ).first()
            serializer = GallerySerializer(
                data={
                    'product': product.id,
                    'img_product': File(open(i, 'rb')),
                },
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def list_product_by_category(self, request):
        category = Category.objects.get(title=request.data['category'])
        queryset = Product.objects.filter(
            category=category,
        ).order_by('-id')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def new_product(self, request):
        queryset = Product.objects.all().order_by('-id')[:10]
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def list_new_product_by_category(self, request):
        category = Category.objects.get(title=request.data['category'])
        queryset = Product.objects.filter(
            category=category,
        ).order_by('-id')[:10]
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
