from abc import ABC
from typing import Any

from mediaichemy.media.media import Media


class SingleMedia(Media, ABC):
    def __init__(self,
                 params: Any = None):
        super().__init__(params=params)

    @property
    def output_dir(self) -> str:
        return self.directory
