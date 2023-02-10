import strawberry

from application.graphql_api.schema.schema import Query

schema = strawberry.Schema(query=Query)
