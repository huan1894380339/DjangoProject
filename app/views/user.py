from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.models import BlackListedToken, CustomerUser
from app.serializers.user import RegisterSerializer, UserSerializer, SignInSerializer, PasswordSerializer
from app.utils import send_email
from app.utils import get_tokens_for_user
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


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

    @action(detail=False, methods=['post'])
    def sign_up(self, request):
        email = request.data['email']
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        user = CustomerUser.objects.get(email=email)
        current_site = get_current_site(request)
        send_email(user, current_site, html='mail.html')
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def sign_in(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomerUser.objects.filter(email=request.data['email']).first()
        login(request, user)
        token = get_tokens_for_user(user)
        return Response(token)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        user = request.user
        serializer_class = self.get_serializer(
            instance=user, data={
                'new_password': request.data['new_password'], 'password': request.data['password'],
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
