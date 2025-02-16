from abc import ABC
from typing import Generic, Type, TypeVar

from sqlalchemy import ColumnElement, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class ItemRepositoryAbstract(ABC, Generic[T]):
    """Абстрактный репозиторий"""

    model: Type[T]

    @classmethod
    async def get_one(cls, db: AsyncSession, item_id: int) -> T | None:
        """Возвращает объект по ID"""
        model_id: ColumnElement = cls.model.id
        result = await db.execute(select(cls.model).filter(model_id == item_id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, db: AsyncSession) -> list[T]:
        """Возвращает все записи"""
        result = await db.execute(select(cls.model))
        return list(result.scalars().all())

    @classmethod
    async def create(cls, db: AsyncSession, item: T) -> T | None:
        """Создаёт запись в БД"""
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    @classmethod
    async def update(cls, db: AsyncSession, item_id: int, **fields) -> T | None:
        """Обновляет переданные поля"""
        item = await cls.get_one(db, item_id)
        if not item:
            return None
        for field, value in fields.items():
            setattr(item, field, value)
        await db.commit()
        await db.refresh(item)
        return item

    @classmethod
    async def delete(cls, db: AsyncSession, item_id: int) -> None:
        """Удаляет запись"""
        item = await cls.get_one(db, item_id)
        if item:
            await db.delete(item)
            await db.commit()
