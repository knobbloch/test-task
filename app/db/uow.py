from contextlib import asynccontextmanager

from .base import session_local

class UnitOfWork:
	def __init__(self, session_factory):
		self._session_factory = session_factory
		self._session = None

	@asynccontextmanager
	async def start(self, do_commit=True):
		self._session = self._session_factory()
		async with self._session.begin():
			try:
				yield self
				if do_commit:
					await self._session.commit()
			except Exception as e:
				await self._session.rollback()
				raise e

	@property
	def session(self):
		return self._session


uow = UnitOfWork(session_local)
