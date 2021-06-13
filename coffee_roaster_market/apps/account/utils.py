from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import User


def encode_uid(pk: bytes) -> str:
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(pk: str) -> str:
    return force_str(urlsafe_base64_decode(pk))


def build_activation_url(user: User) -> str:
    return settings.ACTIVATION_URL.format(
        {"uid": encode_uid(user.pk), "token": default_token_generator.make_token(user)}
    )
