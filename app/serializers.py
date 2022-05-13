
from dataclasses import field
from itertools import product
import os
from django.core.files import File
from pathlib import Path
from unittest.util import _MAX_LENGTH

from traitlets import default
from .models import CustomerUser, Gallery
from rest_framework import serializers
from .models import CustomerUser, Product, gd_storage
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["code", "category", "title", "description", "price",  "active", "img_product"]
    # def to_representation(self, instance):
    #     image_url = None
    #     if instance.img_product:
    #         image_url = instance.img_product.url
    #     return instance.id, instance.title, image_url
    # def pre_save(self, obj: Product):
    #         obj.img_product = self.request.FILES.get('file')
# class Singup_serializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
#     class Meta:
#         model = CustomerUser
#         fields = ['username','email','password','password2']
#         read_only_fields = []
#     def validate(self, attrs):
#         password = self.attrs['password']
#         password2 = self.attrs['password2']
#         if password!= password2:
#             raise serializers.ValidationError({'password':'passwords must match.'})
#         return super().validate(attrs)

#     def create(self, validated_data):

#         return super().create(validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True) 
    class Meta:
        model = CustomerUser
        fields = ['username','email','password','password2']
    def validate_email(self, email):
        existing = CustomerUser.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError("Someone with that email "
                "address has already registered. Was it you?")
        return email
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password confirm not match!.")
        return data
            
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['id','username', 'email']


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["id", "product","img_product"]
    
    # def validate_path(self, path):
    #     files = os.listdir(path)
    #     import ipdb
    #     ipdb.set_trace()
        # for file in files:
        #     codeProduct = Path(file).stem
        #     existing = Gallery.objects.filter(id=codeProduct).first()
    
class ImgSerializer(serializers.Serializer):
    path = serializers.CharField(max_length = 255)
    def update(self, validated_data, instance):
        # import ipdb
        # ipdb.set_trace()
        print(validated_data)
        # instance.img_product = self.validated_data.get('path', instance.img_product)
        instance.img_product = File(open(self.validated_data['path'],'rb'))
        instance.save()

# class ImgSerializer(serializers.Serializer):
#     path = serializers.CharField(max_length = 255)
#     def update(self, validated_data, instance):
#         FileSerializer(data={'img_file': self.validated_data.get('path', instance.img_product)})
#         # import ipdb
#         # ipdb.set_trace()
#         # print(validated_data)
#         # # instance.img_product = open(self.validated_data.get('path', instance.img_product))
#         # # instance.img_product = self.validated_data.get('path', instance.img_product)
#         # with open(self.validated_data.get('path', instance.img_product), 'rb') as fi:
#         #     instance.img_product = File(fi, name=os.path.basename(fi.name))
#         #     instance.save()
 
# class FileSerializer(serializers.ModelSerializer):
#     img_file = serializers.FileField(upload_to='maps/', storage=gd_storage, blank=True)
    


# class SerializerB(serializers.ModelSerializer):
#     pass
#     class Meta:
#         model = Product
#         field = "img_product"
    
#     def update(self, instance, validate_data):
#         print()

# class SerializerA(serializers.Serializer):
#     pass
#     path = serializers.CharField(default='D:\\A')

#     def update(self, validate_data):
#         list_images_ac = ['aaaa']
#         list_image_ap = ['']
#         product_instance = Product.objects.gi
#         products = []
#         for ac in list_images_ac:
#             product = SerializerB(many=False, data=iâ, instance=â)
#             if product.is_valid():
#                 product.save()
#             products.append(product)



"""
# step: 1
# body:
    {
        "path": "D:\Anh"
    }
-> request

views:
    bo no vao serializer(data=request.data)
serializers:
    update:
        validate_data: no dang chua request.data (body) 
        {
            "path": "D:\Anh"
        }
        -> lay danh sach anh chinh va anh phu tu path truyen vao
        se co dinh dang o anh chinh nhu sau:
        [
            {
                "name": "A.png",
                "path_ac": "D:\Anh\AnhChinh\A.png",
                "anh_phu": [
                    {
                        "name": "B.png",
                        "path_ap": "xxx.xxx"
                    }
                ]
            },
        ]
        danh sach anh phu y chang

        -> Loc ten anh chinh xem co san pham (title) giong nhu anh hay khong
        -> chung ta lay duoc san pham do (p)
        -> tu p ta update anh chinh bang cach su dung File(file_object, name): file_object = open(path_ac, mode="rb")
        -> sau do ta save

        for item in danh sach anh chinh:
            filename = item['name']
            path_ac = item['path_ac']
            anhphu= item['anh_phu']
            # Product.objects.filter(title=filenam).update(img_product=File(file_object, name) # khong co signal, co the hk dung dc
            product = Product.object.filter(title=filename).first()
            if product:
                product.img_product = File(file_object, name)
               
                for it in anhphu:
                    product.prod_gallery.img_product=  File(file_object, it['name'])
                product.save() 
            continue
"""
