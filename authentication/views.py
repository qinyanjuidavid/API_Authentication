from django.shortcuts import render
from authentication.send_mail import send_activation_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authentication.serializers import RegistrationSerializer
from rest_framework import status, authentication, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import jwt
from django.conf import settings
from authentication.models import User
from rest_framework_simplejwt.tokens import RefreshToken


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
