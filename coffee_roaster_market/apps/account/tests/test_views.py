import re
from typing import Final

from rest_framework.reverse import reverse
from django.core import mail
from rest_framework import status
from rest_framework.test import APIClient

from coffee_roaster_market.apps.coffee.tests.assets import parse_json_data
from ..models import User

USERS_LIST: Final[str] = "account:user-list"
ACTIVATE_URL: Final[str] = "account:user-activate"
ME_URL: Final[str] = "account:user-me"
FORMAT_JSON: Final[str] = "json"
EXAMPLE_DATA: Final[dict[str, str]] = {
    "username": "Andrzej",
    "email": "hola@exmple.com",
    "password": "hehe",
    "password_retype": "hehe",
}


def test_get_user_list(staff_client: APIClient, users):
    url = reverse(USERS_LIST)
    response = staff_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = parse_json_data(response.content)

    assert len(response_data) == User.objects.all().count()


def test_post_user(client: APIClient, users):
    url = reverse(USERS_LIST)
    data = EXAMPLE_DATA
    response = client.post(url, data, format=FORMAT_JSON)

    assert response.status_code == status.HTTP_201_CREATED
    assert (
        User.objects.filter(username=data["username"], email=data["email"]).count() == 1
    )


def test_post_user_and_activate(client: APIClient, users):
    url_create = reverse(USERS_LIST)
    url_activate = reverse(ACTIVATE_URL)

    data = EXAMPLE_DATA
    response = client.post(url_create, data, format=FORMAT_JSON)
    user = User.objects.filter(username=data["username"]).first()

    assert user is not None
    assert not user.is_active

    mail_text = mail.outbox[0].body
    url = re.findall(r"http\:\/\/.*", mail_text).pop()
    uid, token = url.rsplit("/", 2)[1:]

    response = client.post(
        url_activate, {"token": token, "uid": uid}, format=FORMAT_JSON
    )
    assert response.status_code == status.HTTP_201_CREATED

    user.refresh_from_db()

    assert user.is_active


def test_get_me(client: APIClient):
    url_me = reverse(ME_URL)
    client_username = "someuser"
    response = client.get(url_me)
    assert response.status_code == status.HTTP_200_OK
    response_data = parse_json_data(response.content)
    assert response_data["username"] == client_username


def test_update_me(client: APIClient):
    url_me = reverse(ME_URL)
    new_client_username = "SomeGuy"
    response = client.patch(
        url_me, {"username": new_client_username}, format=FORMAT_JSON
    )
    assert response.status_code == status.HTTP_200_OK

    assert User.objects.filter(username=new_client_username).count() == 1
