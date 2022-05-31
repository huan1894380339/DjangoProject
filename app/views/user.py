from __future__ import annotations

from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.models import BlackListedToken, CustomerUser
from app.serializers.user import RegisterSerializer, UserSerializer, SignInSerializer, PasswordSerializer
from app.utils import send_email
from app.utils import get_tokens_for_user
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class ListUser(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomerUser.objects.all()


class SignUp(GenericAPIView):
    def post(self, request):
        import ipdb
        ipdb.set_trace()
        email = request.data['email']
        serializers = RegisterSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        user = CustomerUser.objects.get(email=email)
        current_site = get_current_site(request)
        send_email(user, current_site)
        return Response(status=status.HTTP_201_CREATED)


class SignIn(GenericAPIView):
    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomerUser.objects.filter(email=request.data['email']).first()
        login(request, user)
        print('IsAuthenticated', user.is_authenticated)
        token = get_tokens_for_user(user)
        return Response(token)


class VerifyAcount(GenericAPIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'is_active': True})


class ChangePassword(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        import ipdb
        ipdb.set_trace()
        user = request.user
        serializer_class = PasswordSerializer(
            instance=user, data={
                'new_password': request.data['new_password'], 'password': request.data['password'],
            },
        )
        serializer_class.is_valid(raise_exception=True)
        serializer_class.update(serializer_class.validated_data, user)
        return Response(status=status.HTTP_200_OK)


class SignOut(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        import ipdb
        ipdb.set_trace()
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
