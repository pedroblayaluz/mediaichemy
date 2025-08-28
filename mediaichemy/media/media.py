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

    @abstractmethod
    def output_dir(self) -> str:
        pass

    @property
    def directory(self) -> str:
        return f"media/{self.name}/"

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()
