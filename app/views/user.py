from __future__ import annotations
import email
from numpy import require

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q
from app.models import BlackListedToken, CustomerUser
from app.serializers.user import RegisterSerializer, UserSerializer, SignInSerializer, PasswordSerializer
from app.utils import send_email, check_acount_email_already, get_tokens_for_user
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from app.authentication import IsTokenValid
from drf_yasg.openapi import (
    Schema,
    TYPE_OBJECT,
    TYPE_STRING,
    TYPE_INTEGER,
    FORMAT_PASSWORD
)
from drf_yasg import openapi

from drf_yasg.utils import swagger_auto_schema
from app.exception import SignUpUserException

class UserViewSet(GenericViewSet):
    queryset = CustomerUser.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'sign_up':
            return RegisterSerializer
        if self.action == 'sign_in':
            return SignInSerializer
        if self.action == 'change_password':
            return PasswordSerializer
        return UserSerializer
    
    @swagger_auto_schema(
        request_body=Schema(
            type=TYPE_OBJECT,
            description='Token generate for user',
            required=['email', 'username', 'password', 'password2'],
            properties={
                'email': Schema(title='Your Email', type=TYPE_STRING, format=TYPE_STRING),
                'username': Schema(title='Your Username', type=TYPE_STRING, format=TYPE_STRING),
                'password': Schema(title='Password', type=TYPE_STRING, format=FORMAT_PASSWORD),
                'password2': Schema(title='Confirm password', type=TYPE_STRING, format=FORMAT_PASSWORD)
            },
        ),
        responses={
            201: 'Create account successfully',
            400: 'Invalid Information, Please check it again'

        }
    )
    @action(detail=False, methods=['post'])
    def sign_up(self, request):
        email = request.data['email']
        if check_acount_email_already(email) is False:
            serializers = self.get_serializer(data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            user = CustomerUser.objects.get(email=email, username=request.data['username'])
            current_site = get_current_site(request)
            send_email(user, current_site, html='mail.html')
            return Response(status=status.HTTP_201_CREATED)
        raise SignUpUserException

    @swagger_auto_schema(
        security=[],
        request_body=Schema(
            type=TYPE_OBJECT,
            description='Token generate for user',
            required=['email_username', 'password'],
            properties={
                'email_username': Schema(title='Your Email/Username', type=TYPE_STRING, format='email'),
                'password': Schema(title='Your Password', type=TYPE_STRING, format=FORMAT_PASSWORD),
            },
        ),
        responses={
            200:Schema(
            type=TYPE_OBJECT,
            properties={
                'access': Schema(title='Access Token', type=TYPE_STRING, format=TYPE_STRING),
                'refresh': Schema(title='Refresh Token', type=TYPE_STRING, format=TYPE_STRING),
            },
        ),
            400: 'Incorrect Email/Username or Password'
        }
    )
    @action(detail=False, methods=['post'])
    def sign_in(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomerUser.objects.get(Q(email=request.data['email_username'])| Q(username=request.data['email_username']), is_active=True)
        login(request, user)
        token = get_tokens_for_user(user)
        return Response(token)

    @swagger_auto_schema(
        security=[{'Bearer': []}],
        request_body=Schema(

            type=TYPE_OBJECT,
            required=['password', 'new_password', 'confirm_password'],
            properties={
                'password': Schema(title='Password', type=TYPE_STRING, format=FORMAT_PASSWORD),
                'new_password': Schema(title='Password', type=TYPE_STRING, format=FORMAT_PASSWORD),
                'confirm_password': Schema(title='Confirm password', type=TYPE_STRING, format=FORMAT_PASSWORD)
            },
        ),
        responses={
            200: 'Password change successful',
            400: openapi.Response(
                description="description status 400",
                examples={
                    "application/json": {
                        "password": "Old Password Incorrect",
                        "confirm_password": "Password new and password confirm not match!",
                    }
                }
                ),

        },
    ) 
    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        user = request.user
        serializer_class = self.get_serializer(
            instance=user, data={
                'new_password': request.data['new_password'], 'password': request.data['password'], 'confirm_password':request.data['confirm_password']
            },
        )
        serializer_class.is_valid(raise_exception=True)
        serializer_class.update(serializer_class.validated_data, user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def sign_out(self, request):
        try:
            refresh_token = request.data['refresh']
            access_token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            BlackListedToken.objects.create(
                token=access_token, user=request.user,
            )
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        user = CustomerUser.objects.get(email=request.data['email'])
        current_site = get_current_site(request)
        send_email(user, current_site, html='mail_reset_password.html')
        return Response({'message': 'Check your email'})

    @action(detail=False, methods=['post'], url_path=r'active_account/<uidb64>/<token>', url_name='active_acount')
    def active_account(request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomerUser._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CustomerUser.DoesNotExist):
            user = None
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response('Thank you for your email confirmation. Now you can login your account.')
        else:
            return Response('Activation link is invalid!')
