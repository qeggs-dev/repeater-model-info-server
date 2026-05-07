from ..._server import Server
from .._route import router
from fastapi.responses import JSONResponse

@router.post("/refresh")
async def refresh_all():
    """
    Refresh all model info from providers
    """
    await Server.core.get_and_populates()
    await Server.core.to_providers_library()
    return JSONResponse(
        content={
            "message": "Model info refreshed successfully",
            "status": "ok"
        },
        status_code=200
    )