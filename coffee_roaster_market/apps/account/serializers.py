from typing import Type, cast
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers

User = get_user_model()
User = cast(Type[AbstractUser], User)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password_retype = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_retype"]

    def validate(self, attrs):
        re_password = attrs.pop("password_retype")
        if attrs["password"] != re_password:
            raise serializers.ValidationError("password mismatch!")
        return super().validate(attrs)

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user
