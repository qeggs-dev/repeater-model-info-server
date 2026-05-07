from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader
from environs import Env
_env = Env()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def verify_api_key(api_key: str | None = Depends(api_key_header)):
    valid_key = _env.str("API_KEY")

    if api_key is None:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "API key is missing"
            }
        )
    elif api_key != f"Bearer {valid_key}":
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Invalid API key"
            }
        )
    
    return {"api_key": api_key}


router = APIRouter(dependencies=[Depends(verify_api_key)])