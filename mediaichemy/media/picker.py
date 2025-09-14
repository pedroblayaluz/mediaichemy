from pydantic import BaseModel, Field
from mediaichemy.ai.llm.agent import AgentAI
import logging

from mediaichemy.media.single import (Image, Video, Narration)
from mediaichemy.media.multi import (VideoFromImage, NarrationWithBackground,
                                     SubtitledNarratedVideo)

logger = logging.getLogger(__name__)

# Simplified media types without parameters
MEDIA_TYPES = {
    "image": (
        Image,
        "Static image generation"),
    "video": (
        Video,
        "Full video generation"),
    "narration": (
        Narration,
        "Audio narration only"),
    "video_from_image": (
        VideoFromImage,
        "Animate a static image"),
    "narration_with_background": (
        NarrationWithBackground,
        "Audio narration with background music"),
    "subtitled_narrated_video": (
        SubtitledNarratedVideo,
        "Video with narration and subtitles")
}

MEDIA_DESCRIPTIONS = "\n".join([f"- {name}: {info[1]}" for name, info in MEDIA_TYPES.items()])


class MediaTypeChoice(BaseModel):
    media_type: str = Field(
        description=f"The chosen media type. Must be one of: {', '.join(MEDIA_TYPES.keys())}"
    )
    reasoning: str = Field(description="Explanation of why this media type was chosen")


class MediaTypePicker(AgentAI):
    def __init__(self, model=None):
        system_prompt = f"""
        You are an expert media format selector. Choose the most appropriate
        media type based on the user's prompt requirements.

        AVAILABLE MEDIA TYPES:
        {MEDIA_DESCRIPTIONS}

        Always choose exactly one media type from the list above.
        """

        super().__init__(
            output_type=MediaTypeChoice,
            system_prompt=system_prompt,
            model=model
        )

    def get_media_type(self, media_type: str):
        """Get the media class for a specific media type"""
        if media_type not in MEDIA_TYPES:
            raise ValueError(f"Unknown media type: {media_type}")

        media_type = MEDIA_TYPES[media_type][0]
        return media_type


async def pick_best_media_type(user_prompt: str):
    media_picker = MediaTypePicker()
    response = await media_picker.create(user_prompt=user_prompt)
    choice = response.output

    media_type = media_picker.get_media_type(choice.media_type)
    logger.info(f"Chosen media type: {choice.media_type} - {choice.reasoning}")
    return media_type
