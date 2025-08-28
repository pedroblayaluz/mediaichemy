from pydantic import BaseModel, Field
from mediaichemy.formulas.formula import ConceptFormula
from mediaichemy.file import VideoFile
from mediaichemy.parameters import Parameters


class CompositeVideoConcept(BaseModel):
    """Represents a single social media post idea with multilingual content."""

    video_prompts: list[str] = Field(description="List containing video prompts for each take.")
    post_caption: str = Field(description="A caption for the social media post.")


class CompositeVideoFormula(ConceptFormula):
    """Formula for generating short video content for social media."""
    def __init__(self,
                 params: Parameters = Parameters()):
        super().__init__(params=params)

    @property
    def concept(self) -> BaseModel:
        return CompositeVideoConcept

    @property
    def system_prompt(self):
        return """You are an expert AI video editor/creator.
        Generate a short video for social media.
        Each short video is composed of AI video takes.
        Each take is around 5 seconds long.
        Calculate the number of takes based on the total duration (divide total duration by 5 and round it).
        Create video prompts for each take, ensuring they are concise and impactful.
        The video should be suitable for platforms like TikTok, Instagram Reels, or YouTube
        Keep image prompts very simple
        Be very very random in the prompts you create,
        in a way that if you tried to create the same video again
        it would be very unlikely to get a similar result."""

    @property
    def prompt_example(self):
        return """Generate 5 short videos with a profound message
                  about the meaning of life in a world where AI is replacing human creativity."""

    async def create(self) -> list[VideoFile]:
        pass  # Placeholder for actual implementation
