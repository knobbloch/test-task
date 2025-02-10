from typing import Any

from sqlalchemy import select, delete, update as sqlalchemy_update, func
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
	model = None

	@classmethod
	async def find_all(cls, session: AsyncSession, **filter_by) -> Any:
		query = select(cls.model).filter_by(**filter_by)
		result = await session.execute(query)
		return result.scalars().all()

	@classmethod
	async def get_by(cls, session: AsyncSession, **filter_by) -> Any:
		query = select(cls.model).filter_by(**filter_by)
		result = await session.execute(query)
		return result.scalars().first()

	@classmethod
	async def count(cls, session: AsyncSession, **filter_by) -> Any:
		query = select(func.count()).select_from(cls.model).filter_by(**filter_by)
		result = await session.execute(query)
		return result.scalar()

	@classmethod
	async def exists(cls, session: AsyncSession, **filter_by) -> bool:
		query = select(func.count()).select_from(cls.model).filter_by(**filter_by)
		result = await session.execute(query)
		return result.scalar() > 0

	@classmethod
	async def insert(cls, session: AsyncSession, obj: model) -> None:
		session.add(obj)
		await session.flush()

	@classmethod
	async def update_object(cls, session: AsyncSession, obj: model) -> None:
		await session.merge(obj)
		await session.flush()

	@classmethod
	async def update_by(cls, session: AsyncSession, filter_by: dict, **values) -> None:
		query = (
			sqlalchemy_update(cls.model)
			.where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
			.values(**values)
			.execution_options(synchronize_session="fetch")
		)
		await session.execute(query)
		await session.flush()

	@classmethod
	async def upsert(cls, session: AsyncSession, filter_by, **values) -> None:
		query = (
			sqlalchemy_update(cls.model)
			.where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
			.values(**values)
			.execution_options(synchronize_session="fetch")
		)

		result = await session.execute(query)
		if result.rowcount == 0:
			obj_to_insert = cls.model(**{**filter_by, **values})
			session.add(obj_to_insert)
		await session.flush()

	@classmethod
	async def delete_object(cls, session: AsyncSession, obj: model) -> None:
		await session.delete(obj)
		await session.flush()

	@classmethod
	async def delete_by(cls, session: AsyncSession, **filter_by) -> None:
		query = delete(cls.model).where(
			*[getattr(cls.model, key) == value for key, value in filter_by.items()]
		)
		await session.execute(query)
		await session.flush()

	@classmethod
	async def get_all(cls, session: AsyncSession) -> Any:
		query = select(cls.model)
		result = await session.execute(query)
		return result.scalars().all()
