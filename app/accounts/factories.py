import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ["email", "username"]

    email = factory.Faker("email", locale="pl_PL")
    username = factory.LazyAttribute(lambda u: u.email.split("@")[0])
    first_name = factory.Faker("first_name", locale="pl_PL")
    last_name = factory.Faker("last_name", locale="pl_PL")
    is_active = True
