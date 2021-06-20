import pytest

from ..models import User


@pytest.fixture
def users():
    return User.objects.bulk_create(
        [
            User(username="usr1", password="pwd", email="elo@example.com"),
            User(username="usr2", password="pwd", email="hi@example.com"),
            User(username="usr3", password="pwd", email="bonjour@example.com"),
        ]
    )
