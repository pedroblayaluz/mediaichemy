from abc import ABC, abstractmethod
import os


class AIService(ABC):
    @abstractmethod
    async def create(self, prompt: str, **kwargs):
        pass

    @staticmethod
    def require_env_var(env_key: str) -> str:
        value = os.getenv(env_key)
        if not value:
            raise ValueError(f"{env_key} environment variable must be set to use this service")
        return value
