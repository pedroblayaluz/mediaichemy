from typing import Type, Optional

from mediaichemy.ai import AgentAI
from mediaichemy.media.type_picker import MediaTypePicker

import logging
logger = logging.getLogger(__name__)


class MediaCreator:
    base_system_prompt = (
        "You are an expert content creator.\n"
        "Create a content outline using the following structure\n"
        "IMPORTANT: Only change attributes with no default values, "
        "keep default values for every other attribute"
    )

    def __init__(self,
                 media_type: Optional[Type] = None,
                 creator_model: str = None):
        self.media_type = media_type
        self.creator_model = creator_model

    @property
    def system_prompt(self) -> str:
        return f"{self.base_system_prompt}\n{self.media_type.instructions}"

    async def create(self, user_prompt: str, **kwargs):
        await self.ensure_media_type(user_prompt)
        self.initialize_agent()
        await self.create_outline(user_prompt=user_prompt)
        if kwargs:
            self.adjust_outline_params(**kwargs)
        await self.create_media()
        await self.create_captions()
        return self.media

    async def ensure_media_type(self, user_prompt: str):
        if self.media_type is None:
            picker = MediaTypePicker(model=self.creator_model)
            self.media_type = await picker.pick(user_prompt)

    def initialize_agent(self):
        self.agent = AgentAI(
            output_type=self.media_type.params_class,
            system_prompt=self.system_prompt,
            model=self.creator_model
        )

    async def create_outline(self, user_prompt: str):
        logger.debug(f"Creating {self.media_type.__name__} outline using AI...")
        response = await self.agent.create(user_prompt=user_prompt)
        self.usage = response.usage()
        self.outline = response.output
        return response

    def _check_outline(self):
        if not hasattr(self, 'outline'):
            raise ValueError("You must run create_outline() first")

    def adjust_outline_params(self, **params):
        self._check_outline()
        for param_name, value in params.items():
            if hasattr(self.outline, param_name):
                setattr(self.outline, param_name, value)
            else:
                logger.warning(f"Parameter '{param_name}' not found in outline - skipping")

        return self.outline

    def initialize_media(self):
        self._check_outline()
        self.media = self.media_type(params=self.outline)
        return self.media

    async def create_media(self):
        self.initialize_media()
        await self.media.create()
        return self.media

    async def create_captions(self):
        self._check_outline()
        return await self.media.create_captions(model=self.creator_model)
