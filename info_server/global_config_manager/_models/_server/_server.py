from pydantic import BaseModel, ConfigDict

class ServerConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    host: str | None = None
    port: int | None = None
    api_key_env: str = "API_KEY"
    workers: int | None = None
    reload: bool | None = None
    run_server: bool = True