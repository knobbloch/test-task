from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.api_key import auth

from app.db.repositories import (OrganizationActivityRepository, OrganizationRepository, ActivityRepository, BuildingRepository)
from app.db.uow import uow

print_router = APIRouter(prefix='/print', tags=['print API'])

@print_router.get('/all_organizations', summary='список всех организаций',)
async def all_organizations():#auth: bool = Depends(auth)):
    async with uow.start(do_commit=False) as uow_session:
        return await OrganizationRepository.get_all(uow_session.session)


@print_router.get('/all_buildings', summary='список всех зданий',)
async def all_buildings():#auth: bool = Depends(auth)):
    async with uow.start(do_commit=False) as uow_session:
        return await BuildingRepository.get_all(uow_session.session)


@print_router.get('/all_activities', summary='список всех деятельностей',)
async def all_activities():#auth: bool = Depends(auth)):
    async with uow.start(do_commit=False) as uow_session:
        return await ActivityRepository.get_all(uow_session.session)


@print_router.get('/all_organizations_activities', summary='список организаций-деятельностей',)
async def all_organizations_activities():#auth: bool = Depends(auth)):
    async with uow.start(do_commit=False) as uow_session:
        return await OrganizationActivityRepository.get_all(uow_session.session)