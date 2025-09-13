from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class VisualParameters(BaseModel):
    width: Literal[1088, 1920] = 1088
    height: Literal[1088, 1920] = 1920


class ImageParameters(VisualParameters):
    image_prompt: str
    image_model: str = "rundiffusion:110@101"


class VideoParameters(VisualParameters):
    video_prompt: str
    video_model: str = 'bytedance:1@1'
    duration: Optional[float] = None


class VideoFromImageParameters(VisualParameters):
    video_prompt: str
    image_model: str = "rundiffusion:110@101"
    video_model: str = 'bytedance:1@1'
    duration: Optional[int] = 6


class NarrationParameters(BaseModel):
    narration_text: str = Field(max_length=300,
                                description="The text to be narrated in the video, limited to 200 characters")
    narration_voice_name: str = "en_US-amy-medium"
    narration_silence_tail: float = 5


class NarrationWithBackgroundParameters(NarrationParameters):
    background_relative_volume: float = 0.5
    background_youtube_urls: List[str] = []


class NarratedVideoParameters(VideoFromImageParameters, NarrationWithBackgroundParameters):
    pass


class SubtitleParameters(BaseModel):
    subtitle_fontname: str = "Verdana"
    subtitle_fontsize: int = 18

    subtitle_color: str = "#FFEE00C7"
    subtitle_outline_color: str = "#000000"

    subtitle_positions: List[str] = Field(default_factory=lambda: ["bottom_center", "top_center", "middle_center"])


class SubtitledNarratedVideoParameters(NarratedVideoParameters, SubtitleParameters):
    pass
