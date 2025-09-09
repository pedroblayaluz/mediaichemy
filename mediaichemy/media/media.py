from abc import ABC, abstractmethod
from typing import Any

from mediaichemy.file import utils
from mediaichemy.studio import Studio


class Media(ABC):
    def __init__(self,
                 params: Any = None):
        self.studio = Studio(params)
        utils.ensure_dir(self.directory)

    @abstractmethod
    def create(self, output_path: str):
        """Create a media object from the given source."""
        pass

    @property
    @abstractmethod
    def output_dir(self) -> str:
        pass

    @property
    def directory(self) -> str:
        return f"media/{self.name}/"

    @property
    def instructions(self) -> str:
        """Override this to add specific instructions on how to create this type of media"""
        return ("")

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    async def create_captions(self):
        return await self.studio.create_captions(self.output_dir)
