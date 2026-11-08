from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from .config import Settings, get_settings
from .repository import OrderRepository
from .service import OrderService


@lru_cache
def get_repository() -> OrderRepository:
    return OrderRepository()


SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_service(
    repository: Annotated[OrderRepository, Depends(get_repository)],
    settings: SettingsDep,
) -> OrderService:
    return OrderService(repository, settings)


ServiceDep = Annotated[OrderService, Depends(get_service)]