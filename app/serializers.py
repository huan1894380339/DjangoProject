import csv
from tkinter import N
from django.core.files import File
from pathlib import Path
from unittest.util import _MAX_LENGTH
import io
from traitlets import default, validate
from .models import CustomerUser, Gallery, Category
from rest_framework import serializers
from .models import CustomerUser, Product, gd_storage
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["code", "category", "title", "description", "price",  "active", "img_product"]

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
        #     existing = Gallery.objects.filter(id=codeProduct).first()1
    
class ImgSerializer(serializers.Serializer):
    path = serializers.CharField(max_length = 255)
    def update(self, validated_data, instance):
        print(validated_data)
        # instance.img_product = self.validated_data.get('path')
        instance.img_product = File(open(self.validated_data['path'],'rb'))
        instance.save()


class CsvSerializer(serializers.Serializer):
    def create(self, validated_data):
        import ipdb
        ipdb.set_trace()
        filecsv = validated_data['file']
        reader = csv.DictReader(io.StringIO(filecsv.read().decode('utf-8')))
        for line in reader:
            Product.objects.create(
                code =  line['code'],
                category =  Category.objects.get(id=line['category']),
                description =  line['description'],
                title =  line['title'],
                price =  line['price']
            )


