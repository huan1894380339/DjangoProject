from __future__ import annotations

from rest_framework import serializers

from app.models import CustomerUser


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True,
    )

    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'password', 'password2']

    def validate_email(self, email):
        existing = CustomerUser.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError(
                'Someone with that email '
                'address has already registered. Was it you?',
            )
        return email

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password confirm not match!.')
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['id', 'username', 'email']
