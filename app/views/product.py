from __future__ import annotations

from pathlib import Path

from django.core.files import File
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.constant import AnhChinh, AnhPhu
from app.models import Category, Product
from app.serializers.gallery import GallerySerializer
from app.serializers.pagination import DefaultPagination
from app.serializers.product import CsvSerializer
from app.serializers.product import ImgSerializer
from app.serializers.product import ProductSerializer
from app.utils import get_list_path_images


class ProductInstance(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = DefaultPagination


class ImportProductFromCSV(GenericAPIView):
    def post(self, request):
        serializer = CsvSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(request.data)
            return Response(status=status.HTTP_200_OK)


class UploadImageProductFromPath(GenericAPIView):
    def post(self, request: Request) -> Response:
        path = request.data['path']
        link_local = get_list_path_images(path)
        for ac_path in link_local.get(AnhChinh):
            product = Product.objects.filter(title=Path(ac_path).stem).first()
            img_product = File(open(ac_path, 'rb'))
            serializer = ImgSerializer(
                instance=product,
                data={'img_product': img_product},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        for ap_path in link_local.get(AnhPhu):
            product = Product.objects.filter(
                title=str(Path(ap_path).stem).split('_')[0],
            ).first()
            serializer = GallerySerializer(
                data={
                    'product': product.id,
                    'img_product': File(open(ap_path, 'rb')),
                },
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(status=status.HTTP_200_OK)


class GetListProductByCategory(GenericAPIView):
    def get(self, request):
        queryset = Category.objects.all()
        serialize = GallerySerializer(queryset, many=True)
        return Response(serialize.data)
