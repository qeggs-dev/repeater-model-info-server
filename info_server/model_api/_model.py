from pydantic import BaseModel, Field
from .models import ModelAPIData
from ._connection_model import HTTPLimit, HTTPTimeouts


class Model(BaseModel):
    name: str = ""
    base_url: str = ""
    url: str = ""
    fetch_models_url: str | None = None
    proxy: str | None = None
    id: str = ""
    uid: str = ""
    api_key: str | None = None
    parent: str = ""
    parent_id: str = ""
    detailed: ModelAPIData = Field(default_factory=ModelAPIData)
    limit: HTTPLimit | None = None
    timeout: int | float | HTTPTimeouts | None = None