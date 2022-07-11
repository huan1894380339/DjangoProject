from __future__ import annotations
from django.db.models import Q
from numpy import require

from rest_framework import serializers

from app.models import CustomerUser


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True,
    )

    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password confirm not match!')
        return data

    def save(self):
        account = CustomerUser(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            is_active=False,
        )
        password = self.validated_data['password']
        account.set_password(password)
        account.save()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'


class SignInSerializer(serializers.Serializer):
    email_username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=12,style={'input_type': 'password'}, write_only=True,)

    def validate(self, data):
        user = CustomerUser.objects.filter(
            Q(email=data['email_username']) | Q(username=data['email_username']),is_active=True
        ).first()
        if not user or user.check_password(data['password']) is False:
            raise serializers.ValidationError('Incorrect Email/Username or Password')
        if user.is_active is False:
            raise serializers.ValidationError('You have to verify acount')
        return data


class PasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=12, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=12,  style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = CustomerUser
        fields = ['password', 'new_password', 'confirm_password']

    def update(self, validated_data, instance):

        if instance.check_password(self.validated_data['password']) is False:
            raise serializers.ValidationError({'password':'Old Password Incorrect'})
        if validated_data['new_password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'confirm_password':'Password new and password confirm not match!'})
        instance.set_password(self.validated_data['new_password'])
        instance.save()


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']
