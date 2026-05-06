from pydantic import BaseModel

class HTTPLimit(BaseModel):
    max_connections: int | None = 100
    max_keepalive_connections: int | None = 20
    keepalive_expiry: int | float | None = 5

class HTTPTimeouts(BaseModel):
    connect: int | float | None = 5
    read: int | float | None = 5
    write: int | float | None = 5
    pool: int | float | None = None