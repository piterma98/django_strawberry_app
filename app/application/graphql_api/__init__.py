import strawberry
from gqlauth.user.queries import UserQueries
from strawberry.types import Info
from strawberry_django_plus.directives import SchemaDirectiveExtension
from strawberry_django_plus.optimizer import DjangoOptimizerExtension

from application.graphql_api.mutations.auth import AuthMutation
from application.graphql_api.schema.schema import BookQuery


@strawberry.type
class Query(BookQuery, UserQueries):
    @strawberry.field
    def user(self, info: Info) -> str:
        return str(info.context.request.user)

    ...


@strawberry.type
class Mutations(AuthMutation):
    ...


schema = strawberry.Schema(
    query=Query,
    mutation=Mutations,
    extensions=[SchemaDirectiveExtension, DjangoOptimizerExtension],
)
