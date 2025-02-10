from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.api_key import auth
from app.api.request_models import Point
from app.api.response_models import EmptyResponse, OrganizationResponse, ActivityResponse
from app.db.models import Activity

from app.db.repositories import (OrganizationActivityRepository, OrganizationRepository, ActivityRepository, BuildingRepository)
from app.db.uow import uow
from pydantic import conint

test_router = APIRouter(prefix='/test', tags=['test API'])

@test_router.get(
    '/all_organizations_in_building',
    summary='список всех организаций находящихся в конкретном здании', response_model=List[OrganizationResponse] | EmptyResponse
)
async def all_organizations(building_id: int, auth: bool = Depends(auth)):
    async with uow.start(do_commit=False) as uow_session:
        return await OrganizationRepository.find_all(uow_session.session, building_id=building_id)


@test_router.get(
    '/all_organizations_with_activity',
    summary='список всех организаций, которые относятся к указанному виду деятельности', response_model=List[OrganizationResponse] | EmptyResponse
)
async def all_organizations_with_activity(activity_id: int, auth: bool = Depends(auth)):
    async with uow.start(do_commit=False) as uow_session:
        return await ActivityRepository.get_linked_organizations(uow_session.session, activity_id)


@test_router.get(
    '/all_organizations_in_radius',
    summary='список организаций, которые находятся в заданном радиусе области относительно указанной точки на карте. список зданий', response_model=List[OrganizationResponse] | EmptyResponse
)
async def all_organizations_with_activity(point: Point = Depends(), radius: conint(gt=0) = 1,  auth: bool = Depends(auth)):
    async with uow.start(do_commit=False) as uow_session:
        organizations = []
        buildings = await BuildingRepository.get_all(uow_session.session)
        for building in buildings:
            distance = ((float(building.latitude) - float(point.latitude)) ** 2 +
                        (float(building.longitude) - float(point.longitude)) ** 2) ** 0.5
            if distance <= radius:
                organizations_building = await OrganizationRepository.find_all(uow_session.session, building_id=building.id)
                organizations.append(organizations_building)
        return organizations


@test_router.get(
    '/organization_by_id',
    summary='вывод информации об организации по её идентификатору', response_model=OrganizationResponse | EmptyResponse
)
async def organization_by_id(organization_id: int, auth: bool = Depends(auth)):
    async with uow.start(do_commit=False) as uow_session:
        return await OrganizationRepository.get_by(uow_session.session, id = organization_id)


@test_router.get(
    '/organization_by_name',
    summary='вывод информации об организации по её названию', response_model=OrganizationResponse | EmptyResponse
)
async def organization_by_name(organization_name: str,  auth: bool = Depends(auth)):
    async with uow.start(do_commit=False) as uow_session:
        return await OrganizationRepository.get_by(uow_session.session, name = organization_name)


@test_router.get(
    '/all_organizations_with_nested_activity',
    summary='список всех организаций, которые относятся к указанному виду деятельности и к вложенному виду деятельности',
    description = 'искать организации по виду деятельности. Например, поиск по виду деятельности «Еда», которая находится на первом уровне дерева, и чтобы нашлись все организации, которые относятся к видам деятельности, лежащим внутри. Т.е. в результатах поиска должны отобразиться организации с видом деятельности Еда, Мясная продукция, Молочная продукция.',
    response_model=List[OrganizationResponse] | EmptyResponse
)
async def all_organizations_with_nested_activity(activity_id: int,  auth: bool = Depends(auth)):
    async with uow.start(do_commit=False) as uow_session:
        return await ActivityRepository.get_linked_organizations_nested(uow_session.session, activity_id)


@test_router.post(
    '/add_activity',
    summary='добавление вложеннной деятельности',
    description = 'Введите parent_id. Если он будет <=0 то parent_id=null. Программа завершится ошибкой, если уровень вложенности больше 3.',
    response_model=List[ActivityResponse] | EmptyResponse
)
async def all_organizations_with_nested_activity(parent_id: int, name: str,  auth: bool = Depends(auth)):
    async with uow.start(do_commit=False) as uow_session:
        ret = await ActivityRepository.insert(uow_session.session, Activity(name=name, parent_id=parent_id))
        return await ActivityRepository.get_all(uow_session.session)
