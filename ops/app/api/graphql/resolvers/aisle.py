import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator

from ops.app.services.aisle.main import AisleService
from ops.app.services.aisle.dto import AisleInput, AisleFilter
from ops.app.api.graphql.types.aisle import Aisle

AisleType: TypeAlias = Annotated[
    "Aisle", strawberry.lazy("ops.app.api.graphql.types.aisle")
]


@strawberry.type
class AisleQueries:
    @strawberry.field
    @staticmethod
    async def aisles(info) -> list["Aisle"]:
        return await AisleService(info.context.session).get_aisles()

    @strawberry.field
    @staticmethod
    async def aisle(info, id: int) -> Optional["Aisle"]:
        return await AisleService(info.context.session).get_aisle(
            AisleFilter(id=id)
        )


@strawberry.type
class AisleMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_aisle(
        info,
        zone_id: int,
        name: str | None = None,
        description: str | None = None,
        type: str | None = "standard",
        active: bool | None = True,
    ) -> "Aisle":
        return await AisleService(info.context.session).upsert_aisle(
            AisleInput(
                zone_id=zone_id,
                name=name,
                description=description,
                type=type,
                active=active,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_aisle(info, id: int) -> bool:
        return await AisleService(info.context.session).delete_aisle(
            AisleInput(id=id)
        )


@strawberry.type
class AisleSubscriptions:
    @strawberry.subscription
    async def aisle_created(self, info) -> AsyncGenerator[AisleType, None]:
        yield

    @strawberry.subscription
    async def aisle_updated(self, info) -> AsyncGenerator[AisleType, None]:
        yield

    @strawberry.subscription
    async def aisle_deleted(self, info) -> AsyncGenerator[int, None]:
        yield
