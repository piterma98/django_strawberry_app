import strawberry
from gqlauth.user.queries import UserQueries
from strawberry_django_plus.directives import SchemaDirectiveExtension

from application.graphql_api.mutations.auth import LoginMutation
from application.graphql_api.schema.schema import BookQuery


@strawberry.type
class Query(BookQuery, UserQueries):
    ...


@strawberry.type
class Mutations(LoginMutation):
    ...


schema = strawberry.Schema(
    query=Query, mutation=Mutations, extensions=[SchemaDirectiveExtension]
)
