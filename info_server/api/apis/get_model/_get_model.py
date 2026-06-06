import asyncio
from ..._server import Server
from .._route import router
from jsonschema import SchemaError
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from ....model_api import Model

class ModelInfoResponse(BaseModel):
    message: str = ""
    models: list[Model] = Field(default_factory=list)

@router.get("/models/{model_id:path}")
async def get_model_info(model_id: str):
    """
    Get model info
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
    return JSONResponse(
        content = ModelInfoResponse(
            message = f"Get Model {model_id} successfully",
            models = models,
        ).model_dump(exclude_none=True),
        status_code=200,
    )