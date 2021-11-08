from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authentication.serializers import RegistrationSerializer
from rest_framework import status, authentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# pip install pyjwt


@api_view(['POST', 'GET'])
def RegisterApiview(request):
    serializer = RegistrationSerializer(
        data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(is_active=True)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status.status.HTTP_400_BAD_REQUEST)
