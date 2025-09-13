from typing import Optional

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from mediaichemy.ai.ai import AIService
from mediaichemy.ai.llm.openrouter_models import OpenrouterModels
from mediaichemy.ai.llm.modelfallback import with_model_fallback

from dotenv import load_dotenv
load_dotenv()


class ChatAI(AIService):
    def __init__(self,
                 model: Optional[str] = None):
        self.openrouter_api_key = self.require_env_var("OPENROUTER_API_KEY")
        self.openrouter_models = OpenrouterModels()
        self.model_list = self._get_model_list()
        self.current_model = model or self.model_list[0]

    def _get_model_list(self):
        return self.openrouter_models.get_cheapest_models()

    def _get_openai_model(self):
        return OpenAIChatModel(
            self.current_model,
            provider=OpenRouterProvider(api_key=self.openrouter_api_key)
        )

    @with_model_fallback
    async def create(self, prompt) -> str:
        agent = Agent(self._get_openai_model())
        result = await agent.run(prompt)
        return result.output
