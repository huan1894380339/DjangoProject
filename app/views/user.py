from __future__ import annotations

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.models import CustomerUser
from app.serializers.user import RegisterSerializer, UserSerializer, SignInSerializer
from app.utils import snake_case, get_code_verify
from app.utils import get_tokens_for_user


class ListUser(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomerUser.objects.all()


class SignUp(GenericAPIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        serializers = RegisterSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        code_verify = get_code_verify()
        serializers.save()
        snake_case(username, email, password, code_verify)
        return Response(status=status.HTTP_201_CREATED)


class SignIn(GenericAPIView):
    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomerUser.objects.filter(email=request.data['email']).first()
        import ipdb
        ipdb.set_trace()
        token = get_tokens_for_user(user)
        return Response(token)


class VerifyAcount(GenericAPIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'is_active': True})
