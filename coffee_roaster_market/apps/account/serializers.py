from typing import Type, cast
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import User

UserModel = get_user_model()
UserModel = cast(Type[User], UserModel)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["username", "email"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password_retype = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = UserModel
        fields = ["username", "email", "password", "password_retype"]

    def validate(self, attrs):
        re_password = attrs.pop("password_retype")
        if attrs["password"] != re_password:
            raise serializers.ValidationError("password mismatch!")
        return super().validate(attrs)

    def create(self, validated_data):
        user = UserModel(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
