from ..._server import Server
from .._route import router
from fastapi.responses import JSONResponse

@router.post("/refresh/{provider_id}")
async def refresh_provider(provider_id: str):
    """
    Refresh all model info from providers
    """
    provider = Server.core.get_provider(provider_id)
    await provider.get_and_populates()
    await Server.core.to_providers_library()
    return JSONResponse(
        content={
            "message": "Model info refreshed successfully",
            "status": "ok"
        },
        status_code=200
    )