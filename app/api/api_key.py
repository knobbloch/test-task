import os
from dotenv import load_dotenv

from fastapi import HTTPException, Request, Header

load_dotenv()
API_KEY  = os.getenv('API_KEY')
print(f"API_KEY: {API_KEY}")

async def auth(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    return True