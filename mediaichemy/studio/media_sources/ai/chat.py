import os
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.exceptions import ModelHTTPError
import asyncio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
from functools import wraps


def with_model_fallback(func):
    @wraps(func)
    async def wrapper(self, *args, model="openrouter/auto", **kwargs):
        models = [model] + [m for m in self.FALLBACK_MODELS if m != model]
        last_exc = None
        for m in models:
            try:
                return await func(self, *args, model=m, **kwargs)
            except ModelHTTPError as e:
                last_exc = e
                if getattr(e, "status_code", None) == 429:
                    await asyncio.sleep(1)
                    continue
            except Exception as e:
                last_exc = e
        raise last_exc or Exception("All models failed")
    return wrapper


class ChatAI:
    FALLBACK_MODELS = [
        "anthropic/claude-3-haiku",
        "openai/gpt-4o-mini",
        "openai/gpt-3.5-turbo",
        "meta-llama/llama-3.1-8b-instruct:free"
    ]

    def __init__(self,
                 openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
                 ):
        self.openrouter_api_key = openrouter_api_key

    def _get_openai_model(self, model: str):
        return OpenAIModel(
            model,
            provider=OpenRouterProvider(api_key=self.openrouter_api_key)
        )

    @with_model_fallback
    async def make_text(self, prompt, model="openrouter/auto") -> str:
        agent = Agent(self._get_openai_model(model))
        result = await agent.run(prompt)
        return result.output

    @with_model_fallback
    async def make_structured(self,
                              output_type,
                              system_prompt: str,
                              user_prompt: str,
                              model: str = "anthropic/claude-3-sonnet"
                              ) -> BaseModel:
        agent = Agent(
            model=self._get_openai_model(model),
            output_type=output_type,
            system_prompt=system_prompt
        )
        return await agent.run(user_prompt)
