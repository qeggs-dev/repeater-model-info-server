import asyncio
from ..._server import Server
from .._route import router
from jsonschema import SchemaError
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from ....model_api import Model
from .request import DisableRequest
from .response import DisableResponse

class ModelInfoResponse(BaseModel):
    message: str = ""
    models: list[Model] = Field(default_factory=list)

@router.post("/disable/{model_id:path}")
async def disable_models(model_id: str, request: DisableRequest):
    """
    Disables a model from the server
    """
    try:
        models = await asyncio.to_thread(Server.core.find_models, model_id)
    except SchemaError as e:
        return JSONResponse(
            content = ModelInfoResponse(
                message = str(e),
            ).model_dump(exclude_none=True),
            status_code=400,
        )
    
    success_count = 0
    total_count = len(models)
    for model in models:
        if model.detailed.disable(timeout = request.timeout):
            success_count += 1

    return JSONResponse(
        content = DisableResponse(
            message = f"Disabled {success_count} models out of {total_count}",
            success = success_count,
            total = total_count,
        ).model_dump(),
        status_code=200,
    )