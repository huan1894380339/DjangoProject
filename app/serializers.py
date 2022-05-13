
from datetime import date
from pyexpat import model
from .models import CustomerUser
from rest_framework import serializers
from .models import CustomerUser, Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "category", "title", "description", "price",  "active", "img_product"]
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