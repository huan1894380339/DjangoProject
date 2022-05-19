import os
from pathlib import Path
from builtins import str
from django.core.files import File
from tablib import Dataset
from .serializers import GallerySerializer, ProductSerializer,RegisterSerializer, UserSerializer, ImgSerializer, CsvSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.generics import GenericAPIView
from .models import CustomerUser, Product
from .utils import snake_case, get_list_path_images
from .resources import ProductResource

class ProductInstance(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
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
    
class ListUser(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomerUser.objects.all()


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


class UploadImage(GenericAPIView):
    def post(self,request):
        path = request.data['path']
        find_folder = os.listdir(path)
        import ipdb
        ipdb.set_trace()
        if find_folder:
            for folder in find_folder:
                if folder=='AnhChinh':
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
                        product = Product.objects.filter(title = str(Path(i).stem)).first()
                        serializer = ImgSerializer(instance=product, data={"path":i})
                        serializer.is_valid(raise_exception=True)
                        serializer.update(serializer.validated_data, product)    
                if folder=='AnhPhu':
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
                        product = Product.objects.filter(title = str(Path(i).stem).split("_", 1)[0]).first()
                        serializer = GallerySerializer(data = {"product":product.id, "img_product":File(open(i,'rb'))})
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
        return Response(status=status.HTTP_200_OK)


class CSVHandle(generics.GenericAPIView):
    def post(self, request):
            import ipdb
            ipdb.set_trace()
            serializer = CsvSerializer(data = request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.create(request.data)
                return Response(status=status.HTTP_200_OK)


class UploadImageView(GenericAPIView):
    def post(self,request):
        path = request.data['path']
        link_local = get_list_path_images(path)
        for i in link_local.get("AnhChinh"):
            product = Product.objects.filter(title = str(Path(i).stem)).first()
            serializer = ImgSerializer(instance=product, data={"path":i})
            serializer.is_valid(raise_exception=True)
            serializer.update(serializer.validated_data, product)    
        for i in link_local.get("AnhPhu"):
            product = Product.objects.filter(title = str(Path(i).stem).split("_", 1)[0]).first()
            serializer = GallerySerializer(data = {"product":product.id, "img_product":File(open(i,'rb'))})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(status=status.HTTP_200_OK)
