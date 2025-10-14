from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index


class Supplier(SQLModel, table=True):
    __tablename__ = "suppliers"
    __table_args__ = (
        Index("idx_suppliers_code", "code"),
        Index("idx_suppliers_name", "name"),
        Index("idx_suppliers_status", "status"),
    )

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(nullable=False, unique=True, index=True)
    name: str = Field(nullable=False, index=True)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    address_line_1: str | None = Field(default=None)
    address_line_2: str | None = Field(default=None)
    city: str | None = Field(default=None)
    province: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    country: str | None = Field(default=None)
    status: str = Field(default="active", nullable=False)
    notes: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
