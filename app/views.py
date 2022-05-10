from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer
from rest_framework.response import Response
from .models import CustomerUser
from rest_framework import status

# Create your views here.
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    print(serializer.is_valid(raise_exception=True))
    print(serializer.error_messages)
    if serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    # if request.method == 'POST':
        # email = CustomerUser.objects.filter(email = request.data['email']).first()
        # if email is None:
        #     serializer = RegisterSerializer(data = request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data)
        #     else:
        #         return Response(serializer.errors)
        # else :
        #     return Response("your email already registed in database")
            
