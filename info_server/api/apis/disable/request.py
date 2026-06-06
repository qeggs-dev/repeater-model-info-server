from pydantic import BaseModel

class DisableRequest(BaseModel):
    timeout: int