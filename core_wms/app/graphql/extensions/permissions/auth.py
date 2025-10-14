import typing
import strawberry
from strawberry.permission import BasePermission

class IsAuthenticated(BasePermission):
    """General base class for GraphQL permissions.

    Not sure what I am doing with this for now, setting up Apollo Router, and figuring out authentication and
    authorization on a bigger level, will come back to this.
    """
    message = "User is not authenticated."

    async def has_permission(
        self, source: typing.Any, info: strawberry.Info, **kwargs
    ) -> bool:
        return True