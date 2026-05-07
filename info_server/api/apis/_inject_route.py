from ._route import router
from .._server import Server

Server.include_router(router)