import ssl
import time
import httpx
import random

from environs import Env
from typing import Callable, Generator
from .models import ModelAPIData, ModelAPIResponse
from ._configs_model import (
    ProviderConfig,
    HTTPLimit,
    HTTPTimeouts
)
from ._model import Model
from loguru import logger

class ModelProvider:
    _env = Env()
    _ssl_context = ssl.create_default_context()

    def __init__(
        self,
        id: str,
        name: str,
        base_url: str,
        endpoint: str,
        api_key_env: str | dict[str, float],
        fetch_models_endpoint: str | None = None,
        proxy: str | None = None,
        models: list[ModelAPIData] | None = None,
        limit: HTTPLimit | None = None,
        timeout: int | float | HTTPTimeouts | None = 600.0,
        client: httpx.AsyncClient | None = None,
    ):
        self._id = id
        self._name = name
        self._base_url = base_url
        self._endpoint: str = endpoint
        self._fetch_models_endpoint = fetch_models_endpoint or "/models"
        self._proxy = proxy
        self._limit = limit
        self._timeout = timeout
        self._api_key_env = api_key_env
        self._models: dict[str, ModelAPIData] = {}

        if models is not None:
            self._models = {model.id: model for model in models}
        self._client = client or httpx.AsyncClient(
            base_url = base_url,
            proxy = proxy,
            timeout = timeout,
            limits = limit or httpx.Limits(
                max_connections = 100,
                max_keepalive_connections = 20,
            ),
            verify = self._ssl_context
        )
    
    @property
    def id(self) -> str:
        return self._id
    
    def uid(self, model_id: str) -> str:
        return f"{self._id}/{model_id}"
    
    @property
    def uids(self) -> list[str]:
        now = time.time_ns()
        return list(f"{self._id}/{model}" for model in self.models_key_gen(now))
    
    @property
    def uid_tuples(self) -> list[tuple[str, str]]:
        now = time.time_ns()
        return list((self._id, model) for model in self.models_key_gen(now))
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def fetch_models_endpoint(self) -> str:
        return self._fetch_models_endpoint

    @property
    def proxy(self) -> str | None:
        return self._proxy
    
    @property
    def models(self) -> list[ModelAPIData]:
        now = time.time_ns()
        return list(self.models_gen(now))
        
    def models_gen(self, now: int) -> Generator[ModelAPIData, None, None]:
        for model in self._models.values():
            if model.disable_to is None:
                yield model
            elif model.disable_to < now:
                model.disable_to = None
                yield model
    
    def models_key_gen(self, now: int) -> Generator[str, None, None]:
        for key, model in self._models.items():
            if model.disable_to is None:
                yield key
            elif model.disable_to < now:
                model.disable_to = None
                yield key
    
    @property
    def limit(self) -> HTTPLimit | None:
        return self._limit
    
    @property
    def timeout(self) -> int | float | HTTPTimeouts | None:
        return self._timeout
    
    @property
    def api_key_env(self) -> str | dict[str, float]:
        return self._api_key_env
    
    @property
    def client(self) -> httpx.AsyncClient:
        return self._client
    
    @property
    def api_keys(self) -> str | None:
        if isinstance(self.api_key_env, str):
            return self._env.str(self.api_key_env, None)
        elif isinstance(self.api_key_env, dict):
            items: list[str] = []
            weights: list[float] = []

            # Make sure that each item has its own weight.
            for key, weight in self.api_key_env.items():
                items.append(key)
                weights.append(weight)
            return random.choices(items, weights=weights, k=1)[0]
        else:
            return None
    
    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_keys}"
        }
    
    def disable(self, model_id: str, timeout: int):
        try:
            self._models[model_id].disable(timeout)
            return True
        except KeyError:
            logger.warning(
                "Model {model_id} not found in provider {provider_id}",
                model_id = model_id,
                provider_id = self.id
            )
            return False
    
    async def get_models(self) -> ModelAPIResponse:
        url = self.fetch_models_endpoint
        response = await self._client.get(
            url,
            headers = self.headers
        )
        response.raise_for_status()
        data = response.json()
        return ModelAPIResponse(**data)
    
    async def get_and_populates(self):
        response = await self.get_models()
        models = response.data
        self._models = {model.id: model for model in models}
    
    def _api_data_to_model(self, api_data: ModelAPIData) -> Model:
        return Model(
            name = api_data.name or api_data.id,
            base_url = self.base_url,
            endpoint = self.endpoint,
            fetch_models_endpoint = self.fetch_models_endpoint,
            proxy = self.proxy,
            id = api_data.id,
            uid = self.uid(api_data.id),
            api_key = self.api_keys,
            parent_id = self.id,
            detailed = api_data,
            parent = self.name,
            timeout = self.timeout
        )
    
    def find_model(self, model_id: str) -> Model | None:
        now = time.time_ns()
        if model_id in self._models:
            model_info = self._models[model_id]
            if model_info.disable_to is None:
                return self._api_data_to_model(model_info)
            elif model_info.disable_to < now:
                model_info.disable_to = None
                return self._api_data_to_model(model_info)
            else:
                return None
        else:
            return None
    
    def match_models(self, matcher: Callable[[str], bool], get_key: Callable[[str], str] = lambda x: x) -> list[Model]:
        now = time.time_ns()
        return [
            self._api_data_to_model(model_info)
            for model_info in self.models_gen(now)
            if matcher(get_key(model_info.id))
        ]
    
    def get_all_models(self) -> list[Model]:
        return [self._api_data_to_model(model_info) for model_info in self.models]
    
    @classmethod
    def from_config(cls, config: ProviderConfig, client: httpx.AsyncClient | None = None) -> "ModelProvider":
        return cls(
            base_url = config.base_url,
            endpoint = config.endpoint,
            fetch_models_endpoint = config.fetch_models_endpoint,
            proxy = config.proxy,
            limit = config.limit,
            timeout = config.timeout,
            name = config.name,
            id = config.id,
            api_key_env = config.api_key_env,
            models = config.models,
            client = client
        )
    
    def to_config(self) -> ProviderConfig:
        return ProviderConfig(
            base_url = self.base_url,
            endpoint = self.endpoint,
            fetch_models_endpoint = self.fetch_models_endpoint,
            proxy = self.proxy,
            limit = self.limit,
            timeout = self.timeout,
            name = self.name,
            id = self.id,
            api_key_env = self.api_key_env,
            models = self.models,
        )
    
    async def close(self):
        logger.info(
            "Closing Provider: {provider_name}({provider_id})",
            provider_name = self.name,
            provider_id = self.id
        )
        await self._client.aclose()