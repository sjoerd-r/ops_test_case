from typing import Any, TypeVar, Generic
from abc import ABC
from sqlmodel import Session, SQLModel
from strawberry.dataloader import DataLoader

T = TypeVar("T", bound=SQLModel)
K = TypeVar("K")


class SQLALoader(Generic[K, T], ABC):
    column: Any = None
    stmt: Any = None

    def __init__(self, session):
        self.session = session

        async def load_fn(keys: list[K]) -> list[T | None]:
            result = await self.session.exec(
                self.stmt.where(self.column.in_(keys))
            )
            entities = result.all()
            entity_dict = {
                getattr(entity, self.column.name): entity
                for entity in entities
            }
            return [entity_dict.get(key) for key in keys]

        self._loader = DataLoader(load_fn=load_fn)

    async def load(self, key: K) -> T | None:
        return await self._loader.load(key)

    async def load_many(self, keys: list[K]) -> list[T | None]:
        return await self._loader.load_many(keys)


class SQLAListLoader(Generic[K, T], ABC):
    column: Any = None
    stmt: Any = None

    def __init__(self, session: Session):
        self.session = session

        async def load_fn(keys: list[K]) -> list[list[T]]:
            result = await session.exec(self.stmt.where(self.column.in_(keys)))
            entities = result.all()
            grouped = {key: [] for key in keys}
            for entity in entities:
                fk_value = getattr(entity, self.column.name)
                if fk_value in grouped:
                    grouped[fk_value].append(entity)
            return [grouped[key] for key in keys]

        self._loader = DataLoader(load_fn=load_fn)

    async def load(self, key: K) -> list[T]:
        return await self._loader.load(key)

    async def load_many(self, keys: list[K]) -> list[list[T]]:
        return await self._loader.load_many(keys)


class SQLAFilteredLoader(Generic[K, T], ABC):
    column: Any = None
    stmt: Any = None
    filter_column: Any = None
    filter_value: Any = None

    def __init__(self, session: Session):
        self.session = session

        async def load_fn(keys: list[K]) -> list[T | None]:
            result = await session.exec(
                self.stmt.where(
                    self.column.in_(keys),
                    self.filter_column == self.filter_value,
                )
            )
            entities = result.all()
            entity_dict = {
                getattr(entity, self.column.name): entity
                for entity in entities
            }
            return [entity_dict.get(key) for key in keys]

        self._loader = DataLoader(load_fn=load_fn)

    async def load(self, key: K) -> T | None:
        return await self._loader.load(key)

    async def load_many(self, keys: list[K]) -> list[T | None]:
        return await self._loader.load_many(keys)