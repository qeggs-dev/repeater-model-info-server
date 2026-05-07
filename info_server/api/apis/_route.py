from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader
from .._server import Server

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def verify_api_key(api_key: str | None = Depends(api_key_header)):
    valid_auth = Server.api_key.get_bearer_auth()

    if api_key is None:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "API key is missing"
            }
        )
    elif api_key != valid_auth:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Invalid API key"
            }
        )
    
    return {"api_key": api_key}


router = APIRouter(dependencies=[Depends(verify_api_key)])