from pydantic import BaseModel, condecimal

class Point(BaseModel):
    latitude: condecimal(ge=-90, le=90)
    longitude: condecimal(ge=-180, le=180)
