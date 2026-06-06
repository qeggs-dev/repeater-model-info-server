from pydantic import BaseModel, Field
from typing import Literal
from .models import ModelAPIData
from ._connection_model import HTTPLimit, HTTPTimeouts

class ProviderConfig(BaseModel):
    base_url: str = ""
    endpoint: str = ""
    fetch_models_endpoint: str = "/models"
    limit: HTTPLimit | None = None
    timeout: int | float | HTTPTimeouts | None = 600.0
    proxy: str | None = None

    name: str = ""
    id: str = ""
    api_key_env: str | dict[str, float] = "API_KEY"
    models: list[ModelAPIData] | None = None
    
class GroupConfig(BaseModel):
    type: Literal["model_group_config.v1"] = "model_group_config.v1"
    providers: list[ProviderConfig] = Field(default_factory=list)
    library_file: str | None = None