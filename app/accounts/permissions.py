import dataclasses
from typing import Any

from graphql import GraphQLResolveInfo
from strawberry import Private
from strawberry_django_plus.permissions import ConditionDirective
from strawberry_django_plus.utils.typing import UserType

from exceptions import AuthenticationError


class IsUserAuthenticated(ConditionDirective):

    """Mark a field as only resolvable by authenticated users."""

    message: Private[str] = dataclasses.field(default="User is not authenticated.")

    def check_condition(
        self, root: Any, info: GraphQLResolveInfo, user: UserType, **kwargs
    ) -> bool:
        if user.is_authenticated and user.is_active:
            return True
        else:
            raise AuthenticationError("Unauthenticated user")
