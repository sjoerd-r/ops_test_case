from strawberry.fastapi import GraphQLRouter
from core_wms.app.graphql.context import get_context
from core_wms.app.graphql.schema import schema
from core_wms.app.config.settings import settings

class GraphQLAppFactory:
    """General base class for our GraphQL application

    Initializing the GraphQL application with the necessities.
    """

    @classmethod
    def create(cls) -> GraphQLRouter:
        return GraphQLRouter(
            schema,
            context_getter=get_context,
            graphiql=settings.graphql.debug,
            debug=settings.graphql.debug,
        )