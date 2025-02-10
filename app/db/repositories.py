from typing import Sequence

from sqlalchemy import select

from .repositories_base import BaseRepository
from .models import (OrganizationActivity, Organization, Activity, Building)
from sqlalchemy.ext.asyncio import AsyncSession

class OrganizationActivityRepository(BaseRepository):
	model = OrganizationActivity


class OrganizationRepository(BaseRepository):
	model = Organization


class ActivityRepository(BaseRepository):
	model = Activity

	@staticmethod
	async def get_nesting_level(session: AsyncSession, obj: 'Activity') -> int:
		level = 0
		current = await ActivityRepository.get_by(session, id=obj.parent_id)

		while current is not None:
			print(current)
			level += 1
			current = await ActivityRepository.get_by(session, id=current.parent_id)

		return level

	@classmethod
	async def insert(cls, session: AsyncSession, obj: model) -> None:
		nesting_level = await cls.get_nesting_level(session, obj)
		if nesting_level >= 3:
			raise ValueError("The nesting level exceeds 3")

		session.add(obj)

		try:
			await session.flush()
		except Exception as e:
			raise RuntimeError("Error when adding an object to the session") from e

	@classmethod
	async def get_linked_organizations(cls, session: AsyncSession, activity_id) -> Sequence[Organization]:
		stmt = (
			select(Organization)
			.join(OrganizationActivity, OrganizationActivity.organization_id == Organization.id)
			.where(OrganizationActivity.activity_id == activity_id)
		)
		result = await session.execute(stmt)
		return result.scalars().all()

	@classmethod
	async def get_linked_organizations_nested(cls, session: AsyncSession, activity_id) -> Sequence[Organization]:
		sub_activities_stmt = (
			select(Activity)
			.filter(Activity.parent_id == activity_id)
		)
		sub_activities_result = await session.execute(sub_activities_stmt)
		sub_activities = sub_activities_result.scalars().all()

		activity_ids = [activity_id] + [activity.id for activity in sub_activities]

		stmt = (
			select(Organization)
			.join(OrganizationActivity, OrganizationActivity.organization_id == Organization.id)
			.filter(OrganizationActivity.activity_id.in_(activity_ids))
			.group_by(Organization.id)
		)

		result = await session.execute(stmt)
		return result.scalars().all()

class BuildingRepository(BaseRepository):
	model = Building