from authentication import serializers
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import authentication, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.models import User
from authentication.send_mail import (send_activation_mail,
                                      send_Password_reset_email)
from authentication.serializers import (RegistrationSerializer,
                                        ResetPasswordEmailRequestSerializer,
                                        SetNewPasswordSerializer)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        # token['email'] = user.email
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST', 'GET'])
def RegisterApiview(request):
    serializer = RegistrationSerializer(
        data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(is_active=True)
        user_data = serializer.data
        send_activation_mail(user_data, request)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status.status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authenticatedUser(request):
    user = request.user
    serializer = RegistrationSerializer(user)
    return Response(serializer.data)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        print(token)
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload['user_id'])
            print("User:::", user)

            if not user.email_verified:
                user.is_active = True
                user.email_verified = True
                user.save()
            return Response({'Email': 'Successfully activated'},
                            status=status.HTTP_200_OK
                            )
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Link Expired'
                             }, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            raise Response({'error': "Invalid Token"},
                           status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def RequestPasswordResetEmail(request):
    if request.method == "POST":
        # data = {'request': request, 'data': request.data}
        serializer = ResetPasswordEmailRequestSerializer(
            data=request.data)
        email = request.data['email']
        # serializer.is_valid(raise_exception=True)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print("USER:::", user)
            send_Password_reset_email(user, request)

        return Response(
            {'Success': 'We have emailed you a link to reset your password'},
            status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'error': 'Token is no longer valid, Please request a new one.'
                },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return Response({
                'Success': True,
                'message': "Credantials valid",
                'uidb64': uidb64,
                'token': token
            },
                status=status.HTTP_200_OK
            )
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'error': 'Token is no longer valid, Please request a new one.'
                },
                    status=status.HTTP_401_UNAUTHORIZED
                )


@api_view(['PATCH', "GET"])
def SetNewPasswordAPIView(request):
    serializer = SetNewPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if request.method == "GET":
        return Response(serializer.data)
    return Response({
        'success': True,
        'message': 'Password Reset was successful'
    },
        status=status.HTTP_200_OK
    )
