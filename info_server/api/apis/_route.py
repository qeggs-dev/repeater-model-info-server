from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from environs import Env
_env = Env()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str | None = Depends(api_key_header)):
    valid_key = _env.str("API_KEY")

    if api_key is None:
        return JSONResponse(
            status_code=401,
            content={
                "message": "API key is missing"
            }
        )
    elif api_key != valid_key:
        return JSONResponse(
            status_code=401,
            content={
                "message": "Invalid API key"
            }
        )
    
    return {"api_key": api_key}


router = APIRouter(dependencies=[Depends(verify_api_key)])