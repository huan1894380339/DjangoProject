from __future__ import annotations
from django.db.models import Q

from rest_framework import serializers

from app.models import CustomerUser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True,
    )

    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        existing = CustomerUser.objects.filter(email=data['email']).first()
        if existing:
            raise serializers.ValidationError(
                'Someone with that email address has already registered. Was it you?',
            )
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
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        user = CustomerUser.objects.filter(
            Q(email=data['email']) | Q(username=data['email']),
        ).first()
        if not user or user.check_password(data['password']) is False:
            raise serializers.ValidationError('Incorrect Email or Password')
        if user.is_active is False:
            raise serializers.ValidationError('You have to verify acount')
        return data


class PasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=128)

    class Meta:
        model = CustomerUser
        fields = ['password', 'new_password']

    def update(self, validated_data, instance):

        if instance.check_password(self.validated_data['password']) is False:
            raise serializers.ValidationError('Old Password Incorrect')
        instance.set_password(self.validated_data['new_password'])
        instance.save()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255)
    access = serializers.CharField(max_length=255)

    def save(self):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
