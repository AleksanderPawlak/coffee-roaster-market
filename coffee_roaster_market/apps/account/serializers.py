from typing import Type, cast
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from rest_framework import serializers
from templated_email import send_templated_mail

from .models import User
from .utils import build_activation_url, decode_uid

UserModel = get_user_model()
UserModel = cast(Type[User], UserModel)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["username", "email", "is_active"]


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
        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        activation_url = build_activation_url(user=user)
        send_templated_mail(
            template_name="activation",
            from_email="team@cofferoaster.com",
            recipient_list=[user.email],
            context={"activation_url": activation_url},
        )
        return user


class UserActivationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate_uid(self, value: str) -> str:
        try:
            decoded_pk = decode_uid(value)
            self.user = User.objects.get(pk=decoded_pk)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise ValidationError("Invalid uid.")
        else:
            if self.user.is_active:
                raise ValidationError("Account already activated.")
            return value

    def validate_token(self, value) -> dict:
        is_token_valid = default_token_generator.check_token(self.user, value)
        if not is_token_valid:
            raise ValidationError("Invalid token.")

        return value
