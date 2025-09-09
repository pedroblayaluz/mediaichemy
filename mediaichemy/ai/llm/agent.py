import os
from typing import Optional

from pydantic import BaseModel
from pydantic_ai import Agent

from mediaichemy.ai.llm.chat import ChatAI
from mediaichemy.ai.llm.modelfallback import with_model_fallback


class AgentAI(ChatAI):
    def __init__(self,
                 output_type: BaseModel,
                 system_prompt: str,
                 model: Optional[str] = None,
                 openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")):
        super().__init__(model=model, openrouter_api_key=openrouter_api_key)
        self.output_type = output_type
        self.system_prompt = system_prompt
        self.agent = self.prepare_agent()

    def _get_model_list(self):
        return self.openrouter_models.get_cheapest_tool_models()

    def prepare_agent(self) -> Agent:
        agent = Agent(
            model=self._get_openai_model(),
            output_type=self.output_type,
            system_prompt=self.system_prompt
        )
        return agent

    def reconnect(self):
        self.agent = self.prepare_agent()

    @with_model_fallback
    async def create(self, user_prompt: str) -> Agent:
        return await self.agent.run(user_prompt=user_prompt)
