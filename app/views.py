from typing import Generic
from urllib import response
from .serializers import ProductSerializer,RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from .models import CustomerUser, Product
from .utils import snake_case
from rest_framework.exceptions import AuthenticationFailed
from .utils import generate_access_token, generate_refresh_token
from rest_framework.permissions import AllowAny, IsAdminUser
class ProductInstance(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"

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
class SignUp(generics.GenericAPIView):
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
