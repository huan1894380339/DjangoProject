from ast import Return
import os
from pathlib import Path
from builtins import str
from django.core.files import File
from tablib import Dataset
from yaml import serialize
from .serializers import GallerySerializer, ProductSerializer,RegisterSerializer, UserSerializer, ImgSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.generics import GenericAPIView
from .models import CustomerUser, Gallery, Product, Category
#EXCEL
from io import TextIOWrapper
import csv
#
from .utils import snake_case
from .resources import ProductResource
from rest_framework.exceptions import AuthenticationFailed
from .utils import generate_access_token, generate_refresh_token
from rest_framework.permissions import AllowAny, IsAdminUser
class ProductInstance(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # lookup_field = "pk"

    # def get_queryset(self):
    #     # original qs
    #     qs = super().get_queryset()
    #     print(self.kwargs['pk']) 
    #     if self.kwargs['pk']:
    #     # filter by a variable captured from url, for example
    #         return qs.filter(pk=self.kwargs['pk']).first()
    #     return qs

    def productViewset(self):
        product = Product.objects.all()
        return product
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk):
        query = self.get_queryset().get(pk=pk)
        print(query)
        serializer = self.get_serializer(instance=query)
        return Response(serializer.data)
    
# Create your views here.
# class ListProduct(viewsets.ModelViewSet):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
    # def get_queryset(self):
    #     for obj in self.queryset:
    #         print(obj.img_product.url)
    #     # return self.queryset
class ListUser(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomerUser.objects.all()

# # class SingUp(generics.CreateAPIView):
# class SingUp(viewsets.ModelViewSet):
class SignUp(GenericAPIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        serializers = RegisterSerializer(data = request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            snake_case(username, email, password)
            return Response(status=status.HTTP_201_CREATED)
        else: 
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ViewProduct(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        product_resource = ProductResource()
        dataset = Dataset()
        new_products = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(new_products.read().decode('utf-8'),format='csv')
            result = product_resource.import_data(dataset, dry_run=True)                                                                 
        elif file_format == 'JSON':
            imported_data = dataset.load(new_products.read().decode('utf-8'),format='json')
            # Testing data import
            result = product_resource.import_data(dataset, dry_run=True) 

        if not result.has_errors():
            # Import now
            product_resource.import_data(dataset, dry_run=False)


# class UploadImages(viewsets.ModelViewSet):
#      def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         return Response(serializer.data)


class UploadImage(GenericAPIView):
    def post(self,request):
        path = request.data['path']
        find_folder = os.listdir(path)
        if find_folder:
            if 'AnhChinh' in find_folder:
                ac_direct =path+'/AnhChinh'
                list_files_ac = os.listdir(ac_direct)
                link_local = []
                if list_files_ac:
                    for i in list_files_ac:
                        ap = ac_direct+'/'+i
                        print(ap)
                        link_local.append(ap)  
                open(link_local[0])
                for i in link_local:
                    # import ipdb
                    # ipdb.set_trace()
                    product = Product.objects.filter(title = str(Path(i).stem)).first()
                    serializer = ImgSerializer(instance=product, data={"path":i})
                    serializer.is_valid(raise_exception=True)
                    serializer.update(serializer.validated_data, product)
                    # gallery = Gallery.objects.filter(product=product.id)
                    # serialize2 = ProductSerializer(gallery)
            if 'AnhPhu' in find_folder:
                ac_direct =path+'/AnhPhu'
                list_files_ac = os.listdir(ac_direct)
                link_local = []
                if list_files_ac:
                    for i in list_files_ac:
                        ap = ac_direct+'/'+i
                        print(ap)
                        link_local.append(ap)  
                open(link_local[0])
                for i in link_local:
                    # import ipdb
                    # ipdb.set_trace()
                    product = Product.objects.filter(title = str(Path(i).stem).split("_", 1)[0]).first()
                    serializer = GallerySerializer(data = {"product":product.id, "img_product":File(open(i,'rb'))})
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    # gallery = Gallery.objects.filter(product=product.id)
                    # serialize2 = ProductSerializer(gallery)
        return Response(status=status.HTTP_200_OK)

import io
class CSVHandleView(generics.GenericAPIView):
    def post(self, request):
        if 'file' in request.FILES:
            file = request.FILES['file'].read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(file))
            products_list = []
            import ipdb
            ipdb.set_trace()
            for line in reader:
                product = {
                    "code": line['code'],
                    "category": line['category'],
                    "description": line['description'],
                    "title": line['title'],
                    "price": line['price']
                }
                serializer = ProductSerializer(data = product)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            # print(request.FILES['file'].name)
            # # import ipdb
            # # ipdb.set_trace()
            # # Handling csv file before save to database
            # # with open(request.FILES['file'], "r") as csvwr:
            # csv_file = csv.reader(request.FILES['file'].read())
            # next(csv_file)  # Skip read csv header
            # products_list = []
            # for line in csv_file:
            #     product = Product
            #     product.code = line[0]
            #     product.category = Category.objects.get(id = line[1])
            #     product.description = line[2]
            #     product.price = line[3]
            #     products_list.append(product)
            # # Save to database
            # for product in products_list:
            #     serializer = ProductSerializer(data = product)
            #     if serializer.is_valid():
            #         serializer.save()
        return Response(status=status.HTTP_200_OK)
    

# Folder: anh chinh - anh phu
# anh chinh: list img 
#   - list img co format: SP_0001.JPG, ... (Ten SP.file type)
# anh phu: list img
#   - list img co format: SP_0001_1.JPG, ... (Ten SP_(Stt anh phu).file type)

