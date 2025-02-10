from typing import Annotated
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column

int_pk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]
str_not_nullable = Annotated[str, mapped_column(String(255), nullable=False)]
str_nullable = Annotated[str, mapped_column(String(255), nullable=True)]
float_not_nullable = Annotated[float, mapped_column(Float, nullable=False)]
float_nullable = Annotated[float, mapped_column(Float, nullable=True)]
