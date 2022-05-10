
from rest_framework import serializers
from .models import CustomerUser
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True) 
    class Meta:
        model = CustomerUser
        fields = ['username','email','password','password2']
        extract_kwargs = {
            'password':{'write_only':True}
            }
    # def validate(self, attrs):
    #     print("b", attrs)
    #     username = attrs['username']
    #     if not username:
    #          raise serializers.ValidationError({'Missing data!'})
    #     email = attrs['email']
    #     if not email:
    #         raise serializers.ValidationError({'Missing data!'})
        
        # return super().validate(attrs)
    def validate_email(self ,value):
        if not value:
            raise serializers.ValidationError({'Missing data!'})
        return value
    

    # def validation_username(value):dd
    #     if not value:
    #         raise serializers.ValidationError({'Missing data!'})
    #     return value
    #  TO DO 11
    def save(self):
        account = CustomerUser(
            username = self.validated_data['username'],
            email = self.validated_data['email'], 
                )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password!= password2:
            raise serializers.ValidationError({'password':'passwords must match.'})
        account.set_password(password)
        account.save()
        return account