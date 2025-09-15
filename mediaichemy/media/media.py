from abc import ABC, abstractmethod
from typing import Any

from mediaichemy.file import utils
from mediaichemy.studio import Studio


class Media(ABC):
    def __init__(self,
                 params: Any = None,
                 **kwargs):
        self.params = self._build_params(params, **kwargs)
        self.studio = Studio(self.params)
        utils.ensure_dir(self.directory)

    def _build_params(self, params, **kwargs):
        if self.params_class is None:
            raise NotImplementedError("Subclasses must define params_class")
        if params is None:
            params = self.params_class(**kwargs)
        return params

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
