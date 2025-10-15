import strawberry

from ops.app.api.graphql.resolvers.aisle import (
    AisleQueries,
    AisleMutations,
    AisleSubscriptions,
)
from ops.app.api.graphql.resolvers.bin import (
    BinQueries,
    BinMutations,
    BinSubscriptions,
)
from ops.app.api.graphql.resolvers.bin_position import (
    BinPositionQueries,
    BinPositionMutations,
    BinPositionSubscriptions,
)
from ops.app.api.graphql.resolvers.pallet import (
    PalletQueries,
    PalletMutations,
    PalletSubscriptions,
)
from ops.app.api.graphql.resolvers.rack import (
    RackQueries,
    RackMutations,
    RackSubscriptions,
)
from ops.app.api.graphql.resolvers.warehouse import (
    WarehouseQueries,
    WarehouseMutations,
    WarehouseSubscriptions,
)
from ops.app.api.graphql.resolvers.zone import (
    ZoneQueries,
    ZoneMutations,
    ZoneSubscriptions,
)


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


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
