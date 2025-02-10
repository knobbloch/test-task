import asyncio
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.print_api import print_router
from app.api.api import test_router
from app.db import base

DATABASE_URL = 'postgresql://postgres:postgres@test-db:5432/test'


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(print_router, prefix='/print', tags=['print API'])
app.include_router(test_router, prefix='/test', tags=['test API'])



