from abc import ABC, abstractmethod


class AIService(ABC):
    @abstractmethod
    async def create(self, prompt: str, **kwargs):
        pass
