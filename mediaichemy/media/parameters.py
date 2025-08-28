from typing import Optional
from pydantic.dataclasses import dataclass
from dataclasses import field
import pysubs2
from typing import List


@dataclass
class VisualParameters:
    width: int = 1088
    height: int = 1920


@dataclass
class ImageParameters(VisualParameters):
    image_prompt: str = ''
    image_model: str = "rundiffusion:110@101"


@dataclass
class VideoParameters(VisualParameters):
    video_prompt: str = ''
    video_model: str = 'bytedance:1@1'
    duration: float = None


@dataclass
class VideoFromImageParameters(VisualParameters):
    video_prompt: str = ''
    image_model: str = "rundiffusion:110@101"
    video_model: str = 'bytedance:1@1'
    duration: Optional[int] = 6


@dataclass
class SpeechParameters:
    narration_text: str = ''
    voice_name: str = "en_US-amy-medium"
    silence_tail: float = 5


@dataclass
class YoutubeAudioParameters:
    youtube_urls: list[str] = field(default_factory=list)


@dataclass
class SpeechWithBackgroundParameters(SpeechParameters, YoutubeAudioParameters):
    relative_volume: float = 0.5


@dataclass
class NarratedVideoWithBackgroundParameters(VideoFromImageParameters, SpeechWithBackgroundParameters):
    pass


@dataclass
class SubtitleParameters:
    fontname: str = "Verdana"
    fontsize: int = 18

    primarycolor: str = "255,255,0,0"
    secondarycolor: str = "255,255,0,0"
    outlinecolor: str = "0,0,0,0"
    backcolor: str = "0,0,0,128"

    bold: bool = False
    italic: bool = False
    underline: bool = False
    strikeout: bool = False

    scalex: int = 100
    scaley: int = 100
    spacing: int = 0
    angle: int = 0

    borderstyle: int = 1
    outline: float = 0.3
    shadow: float = 1.0

    alignments_map = {
                "bottom_left": pysubs2.Alignment.BOTTOM_LEFT,
                "bottom_center": pysubs2.Alignment.BOTTOM_CENTER,
                "bottom_right": pysubs2.Alignment.BOTTOM_RIGHT,
                "middle_left": pysubs2.Alignment.MIDDLE_LEFT,
                "middle_center": pysubs2.Alignment.MIDDLE_CENTER,
                "middle_right": pysubs2.Alignment.MIDDLE_RIGHT,
                "top_left": pysubs2.Alignment.TOP_LEFT,
                "top_center": pysubs2.Alignment.TOP_CENTER,
                "top_right": pysubs2.Alignment.TOP_RIGHT,
            }
    alignments: List[str] = field(default_factory=lambda: ["bottom_center", "top_center", "middle_center"])

    margin_l: int = 10
    margin_r: int = 10
    margin_v: int = 20


@dataclass
class SubtitledNarratedVideoParameters(NarratedVideoWithBackgroundParameters, SubtitleParameters):
    pass
