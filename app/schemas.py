from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class DrinkSize(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"


class OrderStatus(str, Enum):
    pending = "pending"
    ready = "ready"
    completed = "completed"


class SortBy(str, Enum):
    created_at = "created_at"
    drink = "drink"


class OrderCreate(BaseModel):
    """Что присылает клиент при создании заказа."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    drink: str = Field(
        min_length=1,
        max_length=100,
        description="Название напитка из меню",
        examples=["Латте"],
    )
    size: DrinkSize = Field(description="Размер напитка", examples=["medium"])
    quantity: int = Field(gt=0, description="Количество порций", examples=[2])
    customer_name: str | None = Field(
        default=None,
        max_length=100,
        description="Имя клиента (необязательно)",
        examples=["Ирина"],
    )


class OrderUpdate(BaseModel):
    """Частичное обновление: все поля необязательные."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    drink: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Название напитка из меню",
        examples=["Капучино"],
    )
    size: DrinkSize | None = Field(
        default=None, description="Размер напитка", examples=["large"]
    )
    quantity: int | None = Field(
        default=None, gt=0, description="Количество порций", examples=[3]
    )
    customer_name: str | None = Field(
        default=None,
        max_length=100,
        description="Имя клиента",
        examples=["Анна"],
    )
    status: OrderStatus | None = Field(
        default=None, description="Статус заказа", examples=["ready"]
    )


class Order(BaseModel):
    """Заказ в ответе сервера (с id, статусом и временем создания)."""

    id: int = Field(description="Идентификатор заказа", examples=[1])
    drink: str = Field(description="Название напитка из меню", examples=["Латте"])
    size: DrinkSize = Field(description="Размер напитка", examples=["medium"])
    quantity: int = Field(description="Количество порций", examples=[2])
    customer_name: str | None = Field(
        default=None, description="Имя клиента", examples=["Ирина"]
    )
    status: OrderStatus = Field(
        default=OrderStatus.pending, description="Статус заказа", examples=["pending"]
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Время создания заказа (ставит сервер)",
        examples=["2026-07-10T09:15:00"],
    )