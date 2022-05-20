from __future__ import annotations

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.models import CustomerUser
from app.serializers.user import RegisterSerializer
from app.serializers.user import UserSerializer
from app.utils import snake_case


class ListUser(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomerUser.objects.all()


class SignUp(GenericAPIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        serializers = RegisterSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            snake_case(username, email, password)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
