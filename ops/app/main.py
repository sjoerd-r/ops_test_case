from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import strawberry
from strawberry.fastapi import BaseContext, GraphQLRouter

from ops.app.graphql.schemas.aisle.main import (
    AisleQueries,
    AisleMutations,
    AisleSubscriptions,
)
from ops.app.graphql.schemas.bin.main import (
    BinQueries,
    BinMutations,
    BinSubscriptions,
)
from ops.app.graphql.schemas.bin.position import (
    BinPositionQueries,
    BinPositionMutations,
    BinPositionSubscriptions,
)
from ops.app.graphql.schemas.pallet.main import (
    PalletQueries,
    PalletMutations,
    PalletSubscriptions,
)
from ops.app.graphql.schemas.rack.main import (
    RackQueries,
    RackMutations,
    RackSubscriptions,
)
from ops.app.graphql.schemas.warehouse.main import (
    WarehouseQueries,
    WarehouseMutations,
    WarehouseSubscriptions,
)
from ops.app.graphql.schemas.zone.main import (
    ZoneQueries,
    ZoneMutations,
    ZoneSubscriptions,
)
import os
from types import SimpleNamespace  # Deleted: no longer used as context
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession
from dotenv import load_dotenv

# Optional: dataloaders for nested resolvers (can be expanded gradually)
from ops.app.graphql.dataloaders.aisle import AisleLoaders
from ops.app.graphql.dataloaders.bin import BinLoaders, BinPositionLoaders
from ops.app.graphql.dataloaders.pallet import PalletLoaders, PalletStockLoaders
from ops.app.graphql.dataloaders.rack import RackLoaders
from ops.app.graphql.dataloaders.warehouse import WarehouseLoaders
from ops.app.graphql.dataloaders.zone import ZoneLoaders


@strawberry.type
class Query(
    AisleQueries,
    BinQueries,
    BinPositionQueries,
    PalletQueries,
    RackQueries,
    WarehouseQueries,
    ZoneQueries,
):
    pass


@strawberry.type
class Mutation(
    AisleMutations,
    BinMutations,
    BinPositionMutations,
    PalletMutations,
    RackMutations,
    WarehouseMutations,
    ZoneMutations,
):
    pass


@strawberry.type
class Subscription(
    AisleSubscriptions,
    BinSubscriptions,
    BinPositionSubscriptions,
    PalletSubscriptions,
    RackSubscriptions,
    WarehouseSubscriptions,
    ZoneSubscriptions,
):
    pass


schema = strawberry.Schema(
    query=Query, mutation=Mutation, subscription=Subscription
)

load_dotenv()
DATABASE_URL = (os.getenv("database_url") or os.getenv("DATABASE_URL") or "").strip()
engine = create_async_engine(DATABASE_URL) if DATABASE_URL else None
SessionLocal = (
    async_sessionmaker(
        engine, class_=SQLModelAsyncSession, expire_on_commit=False
    )
    if engine
    else None
)


class CustomContext(BaseContext):
    def __init__(self, session, loaders):
        self.session = session
        self.loaders = loaders


async def get_context() -> CustomContext:
    if SessionLocal is None:
        raise RuntimeError("Missing database_url (or DATABASE_URL) environment variable")
    session = SessionLocal()
    loaders = SimpleNamespace(
        aisle=AisleLoaders(session),
        bin=BinLoaders(session),
        bin_position=BinPositionLoaders(session),
        pallet=PalletLoaders(session),
        pallet_stock=PalletStockLoaders(session),
        rack=RackLoaders(session),
        warehouse=WarehouseLoaders(session),
        zone=ZoneLoaders(session),
    )
    return CustomContext(session=session, loaders=loaders)


def create_app() -> FastAPI:
    app = FastAPI(title="ops", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    graphql_router = GraphQLRouter(schema, path="/graphql", context_getter=get_context)
    app.include_router(graphql_router)

    return app

app = create_app()

