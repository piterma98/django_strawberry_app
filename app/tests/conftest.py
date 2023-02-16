import pytest
from django.test import Client
from pytest_factoryboy import register
from strawberry_django_plus.test.client import TestClient

from accounts.factories import UserFactory

register(UserFactory)


@pytest.fixture
def graphql_client(client: Client) -> TestClient:
    return TestClient(path="/graphql/")
