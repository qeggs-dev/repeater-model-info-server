from pydantic import BaseModel

class DisableResponse(BaseModel):
    message: str = ""
    success: bool = False