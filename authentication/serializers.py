from rest_framework import serializers
from authentication.models import User
from django.db import transaction


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
            # is_active=True,
        )
        password = validated_data['password']
        user.set_password(password)
        user.save()
        return user
