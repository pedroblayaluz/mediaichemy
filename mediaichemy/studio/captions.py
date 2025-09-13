from pydantic import BaseModel, Field
from typing import Optional, List
from mediaichemy.ai.llm.agent import AgentAI
import logging
logger = logging.getLogger(__name__)


class SocialMediaCaption(BaseModel):
    caption: str = Field(description='Post caption')


class YouTubeShortsCaption(SocialMediaCaption):
    caption: str = Field(
        description='Shorts caption (30-70 chars). Use CAPS for keywords, numbers, and questions. '
                    'Create curiosity gaps and clickbait elements. Example: "This ONE TRICK will 10X your results 🔥"'
    )


class InstagramReelsCaption(SocialMediaCaption):
    caption: str = Field(
        description='Reels caption (50-125 chars). Include clear call-to-action, 3-5 relevant hashtags, and emojis. '
                    'Keep tone conversational and authentic. Use simple and popular hashtags rather than specific ones'
                    'Example: "Try this technique today! Double tap if you agree ❤️ #trending #viral #reels"'
    )


class TikTokCaption(SocialMediaCaption):
    caption: str = Field(
        description='TikTok caption (max 150 chars). Focus on strong CTA, trending hashtags, and casual tone. '
                    'Use the simplest and most popular hashtags possible - avoid specific niche hashtags. '
                    'Be direct and concise. Example: "Wait for the end! ↓ Follow for more tips #fyp #viral #trending"'
    )


class Captions(BaseModel):
    """Composite model containing captions for multiple platforms"""
    youtube: Optional[YouTubeShortsCaption] = None
    instagram: Optional[InstagramReelsCaption] = None
    tiktok: Optional[TikTokCaption] = None

    def to_string(self) -> str:
        output = []
        output.append("Youtube")
        if self.youtube:
            output.append(f"{self.youtube.caption}")
        output.append("")
        output.append("Tiktok")
        if self.tiktok:
            output.append(f"{self.tiktok.caption}")
        output.append("")
        output.append("Instagram")
        if self.instagram:
            output.append(f"{self.instagram.caption}")
        return "\n".join(output)


class CaptionMaker:
    system_prompt = (
        "You are an expert social media caption copywriter.\n"
        "Create engaging captions that match each platform's style and audience.\n"
    )

    def __init__(self,
                 parameters: BaseModel,
                 platforms: List[str] = ['youtube_shorts', 'instagram_reels', 'tiktok'],
                 model: Optional[str] = None):
        self.parameters = parameters
        self.platforms = platforms
        self.agent = AgentAI(output_type=Captions,
                             system_prompt=self.system_prompt,
                             model=model)

    def extract_content_from_parameters(self) -> str:
        parameters_dict = self.parameters.model_dump()
        relevant_content_params = [(name, value) for name, value in parameters_dict.items()
                                   if self._relevant_content_parameter(name)]
        formatted_params = [f"{name}: {value}" for name, value in relevant_content_params]
        return "CONTENT TO GENERATE CAPTIONS TO: \n" + "\n".join(formatted_params)

    def _relevant_content_parameter(self, name) -> bool:
        relevant_content_terms = ['text', 'prompt']
        return (isinstance(name, str) and
                any(term.lower() in name.lower() for term in relevant_content_terms))

    async def create_captions_from_parameters(self) -> Captions:
        content = self.extract_content_from_parameters()
        logger.debug(f"Extracted content for caption generation: {content}")
        response = await self.agent.create(user_prompt=content)
        return response.output
