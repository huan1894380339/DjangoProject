from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q
from app.models import BlackListedToken, CustomerUser
from app.serializers.user import RegisterSerializer, UserSerializer, SignInSerializer, PasswordSerializer
from app.utils import send_email, check_account_email_already, get_tokens_for_user
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, logout
from rest_framework.decorators import action
from app.authentication import IsTokenValid
from drf_yasg.openapi import (
    Schema,
    TYPE_OBJECT,
    TYPE_STRING,
    FORMAT_PASSWORD,
)

from drf_yasg.utils import swagger_auto_schema, no_body
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
        security=[],
        operation_summary='Register Account',
        request_body=Schema(
            type=TYPE_OBJECT,
            description='Generate token for user',
            required=['email', 'username', 'password', 'password2'],
            properties={
                'email': Schema(title='Your Email', type=TYPE_STRING, format='email', description='A Email create multiple account with different username, but only one account with this email can be actived', example='17520528@gm.uit.edu.vn'),
                'username': Schema(
                    title='Your Username', type=TYPE_STRING, format=TYPE_STRING, pattern='^[/w.@+-]+$', maxLength=150, minLength=1,
                    description='Username is unique in system, A username is used only for 1 account. This value may contain only letters, numbers, and @/./+/-/_ characters.', example='UserName1',
                ),
                'password': Schema(title='Password', type=TYPE_STRING, format=FORMAT_PASSWORD, example='123'),
                'password2': Schema(title='Confirm password', type=TYPE_STRING, format=FORMAT_PASSWORD, description='Password and confirm password have to same string', example='123'),
            },

        ),
        responses={
            201: 'Create account successfully',
            400: 'Invalid Information, Please check it again',

        },
    )
    @action(detail=False, methods=['post'])
    def sign_up(self, request):
        email = request.data['email']
        if check_account_email_already(email) is False:
            serializers = self.get_serializer(data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            user = CustomerUser.objects.get(
                email=email, username=request.data['username'],
            )
            current_site = get_current_site(request)
            send_email(user, current_site, html='mail.html')
            return Response(status=status.HTTP_201_CREATED)
        raise SignUpUserException

    @swagger_auto_schema(
        security=[],
        operation_summary='Sign In',
        request_body=Schema(
            type=TYPE_OBJECT,
            description='Token generate for user',
            required=['email_username', 'password'],
            properties={
                'email_username': Schema(title='Your Email/Username', type=TYPE_STRING, format='email', description=' Use email or username to signIn.', example='17520528@gm.uit.edu.vn'),
                'password': Schema(title='Your Password', type=TYPE_STRING, format=FORMAT_PASSWORD, example='123'),
            },
        ),
        responses={
            200: Schema(
                type=TYPE_OBJECT,
                properties={
                    'access': Schema(title='Access Token', type=TYPE_STRING, format=TYPE_STRING),
                    'refresh': Schema(title='Refresh Token', type=TYPE_STRING, format=TYPE_STRING),
                },
            ),
            400: 'Incorrect Email/Username or Password',
        },
    )
    @action(detail=False, methods=['post'])
    def sign_in(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomerUser.objects.get(
            Q(email=request.data['email_username']) | Q(
                username=request.data['email_username'],
            ), is_active=True,
        )
        login(request, user)
        token = get_tokens_for_user(user)
        return Response(token)

    @swagger_auto_schema(
        security=[{'Bearer': []}],
        operation_summary='Change Password',
        request_body=Schema(

            type=TYPE_OBJECT,
            required=['password', 'new_password', 'confirm_password'],
            properties={
                'password': Schema(title='Password', type=TYPE_STRING, format=FORMAT_PASSWORD, description='Old password'),
                'new_password': Schema(title='Password', type=TYPE_STRING, format=FORMAT_PASSWORD, description='New password'),
                'confirm_password': Schema(title='Confirm password', type=TYPE_STRING, format=FORMAT_PASSWORD, description='Enter password again to confirm password.'),
            },
        ),
        responses={
            200: 'Password change successful',
            400: Schema(
                type=TYPE_OBJECT,
                properties={
                    'field_error': Schema(title='Message', type=TYPE_STRING, format=TYPE_STRING),
                },
            ),

        },
    )
    @action(detail=False, methods=['put'], permission_classes=[IsTokenValid])
    def change_password(self, request):
        user = request.user
        serializer_class = self.get_serializer(
            instance=user, data={
                'new_password': request.data['new_password'], 'password': request.data['password'], 'confirm_password': request.data['confirm_password'],
            },
        )
        serializer_class.is_valid(raise_exception=True)
        serializer_class.update(serializer_class.validated_data, user)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        security=[{'Bearer': []}],
        operation_summary='Sign Out',
        request_body=no_body,
        responses={
            200: 'Logout successfully',
            400: 'Bad request',
        },
    )
    @action(detail=False, methods=['post'], permission_classes=[IsTokenValid])
    def sign_out(self, request):
        try:
            access_token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            BlackListedToken.objects.create(
                token=access_token, user=request.user,
            )
            logout(request)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        security=[{'Bearer': []}],
        operation_summary='Reset Password',
        request_body=Schema(
            type=TYPE_OBJECT,
            required=['email'],
            properties={
                'email': Schema(title='Password', type=TYPE_STRING, format='email', description='Email account need to reset password'),
            },
        ),
        responses={
            200: 'Password reset successfully, check you email',
            400: 'Bad request',
        },
    )
    @action(detail=False, methods=['post'], permission_classes=[IsTokenValid])
    def reset_password(self, request):
        user = CustomerUser.objects.get(
            email=request.data['email'], is_active=True,
        )
        current_site = get_current_site(request)
        send_email(user, current_site, html='mail_reset_password.html')
        return Response({'message': 'Check your email'})

    # @action(detail=False, methods=['post'], url_path=r'active_account/<uidb64>/<token>', url_name='active_acount')
    # def active_account(request, uidb64, token):
    #     try:
    #         uid = urlsafe_base64_decode(uidb64).decode()
    #         user = CustomerUser._default_manager.get(pk=uid)
    #     except(TypeError, ValueError, OverflowError, CustomerUser.DoesNotExist):
    #         user = None
    #     if user and default_token_generator.check_token(user, token):
    #         user.is_active = True
    #         user.save()
    #         return Response('Thank you for your email confirmation. Now you can login your account.')
    #     else:
    #         return Response('Activation link is invalid!')
