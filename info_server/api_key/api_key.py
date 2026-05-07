import secrets
from environs import Env, EnvError
from loguru import logger

class APIKey:
    _env = Env()

    def __init__(self, api_key_env: str = "API_KEY"):
        self._api_key: str = ""
        try:
            self.load_from_env(api_key_env)
        except EnvError:
            self.generate_api_key()
            logger.warning(
                "API Key not found in environment variables, generating a new one: {api_key}",
                api_key = self._api_key
            )
        
        if not self._api_key:
            logger.error(
                "API Key can't load."
            )
    
    def load_from_env(self, api_key_env: str = "API_KEY"):
        self._api_key = self._env.str(api_key_env)
    
    def get_api_key(self) -> str:
        return self._api_key
    
    def get_bearer_auth(self) -> str:
        return f"Bearer {self._api_key}"
    
    def generate_api_key(self) -> str:
        self._api_key = f"sk-{secrets.token_hex(32)}"
        return self._api_key
    
