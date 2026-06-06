import asyncio
from ..._server import Server
from .._route import router
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from ....model_api import Model
from .request import DisableRequest
from .response import DisableResponse

class ModelInfoResponse(BaseModel):
    message: str = ""
    models: list[Model] = Field(default_factory=list)

@router.post("/disable/{provider_id}/{model_id}")
async def disable_models(provider_id: str, model_id: str, request: DisableRequest):
    """
    Disables a model from the server
    """
    provider = Server.core.providers.get(provider_id)
    success = provider.disable(model_id, request.timeout)

    if not success:
        return JSONResponse(
            content = DisableResponse(
                message = f"Failed to disable model {provider_id}/{model_id}.",
                success = False
            ).model_dump(),
            status_code=400,
        )
    else:
        return JSONResponse(
            content = DisableResponse(
                message = f"Successfully disabled model {provider_id}/{model_id}.",
                success = True
            ).model_dump(),
            status_code=200,
        )