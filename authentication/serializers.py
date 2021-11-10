from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from authentication.models import User
from authentication.send_mail import send_Password_reset_email


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=63, min_length=6, write_only=True
    )
    password_confirmation = serializers.CharField(
        max_length=63, min_length=6, write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirmation')

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')
        if (password and password_confirmation
                and password != password_confirmation):
            raise serializers.ValidationError(
                {'Error': ('Passwords don\'t match!')}
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'Error': ('Email already exists!')}
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'Error': ('Username already exists!')}
            )
        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=False
        )
        password = validated_data['password']
        user.set_password(password)
        user.save()
        return user


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=155, min_length=2)

    class Meta:
        fields = ['email', ]

    def validate(self, attrs):
        # email = attrs['data'].get('email', '')
        # email = self.data.get('email')
        # print(email)
        # request = self.context.get("request")
        # request = attrs['data'].request
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)

    password_confirmation = serializers.CharField(
        min_length=6, max_length=68, write_only=True
    )
    token = serializers.CharField(
        min_length=1, write_only=True
    )
    uidb64 = serializers.CharField(
        min_length=1, write_only=True
    )

    class Meta:
        fields = ('password', 'password_confirmation', 'token', 'uidb64')

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password_confirmation = attrs.get('password_confirmation')
            if (password and password_confirmation
                    and password != password_confirmation):
                raise serializers.ValidationError(
                    {'Error': ('Passwords don\'t match!')}
                )
            token = attrs.get('token')
            uidb64 = attrs.get("uidb64")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)
            user.set_password(password)
            user.save()
        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)
        return super().validate(attrs)
