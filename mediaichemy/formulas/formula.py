from mediaichemy.file import File
from abc import ABC, abstractmethod
from pydantic import BaseModel
from mediaichemy.studio.old_studio import AichemyStudio
from mediaichemy.parameters import Parameters


class MediaFormula(ABC):
    def __init__(self,
                 params: Parameters = Parameters()):
        self.studio = AichemyStudio(self)
        self.params = params

    @abstractmethod
    async def create(self) -> File:
        """Create the media content based on the transmutated formula."""
        pass


class ConceptFormula(MediaFormula):
    def __init__(self,
                 params: Parameters = Parameters()):
        super().__init__(params=params)

    @property
    @abstractmethod
    def concept(self) -> BaseModel:
        """Return the concept for this formula."""
        pass

    @property
    @abstractmethod
    def system_prompt(self):
        """Return the system prompt for this formula."""
        pass

    @property
    @abstractmethod
    def prompt_example(self):
        """Return the model to be used for this formula."""
        pass
