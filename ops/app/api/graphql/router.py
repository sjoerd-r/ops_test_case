from strawberry.fastapi import GraphQLRouter

from ops.app.api.graphql.schema import schema
from ops.app.api.graphql.context import get_context

router = GraphQLRouter(schema, path="/graphql", context_getter=get_context)
