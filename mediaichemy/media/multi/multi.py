from typing import Any
from abc import ABC

from mediaichemy.media.media import Media
from mediaichemy.file import utils, File


class MultiMedia(Media, ABC):
    def __init__(self,
                 params: Any = None):
        super().__init__(params=params)
        self.create_subdirectory()

    def create_subdirectory(self):
        subdirectory = self.directory + self.name
        self.subdirectory = utils.get_next_available_path(subdirectory)
        utils.ensure_dir(self.subdirectory)

    @property
    def output_dir(self) -> str:
        return self.subdirectory + "/"

    def unpack(self, ready_media: File) -> File:
        _, name, ext = ready_media.split_name()
        final_path = self.directory + name + ext
        final_path = utils.get_next_available_path(final_path)
        final_file = ready_media.copy(final_path)
        ready_media.delete()
        utils.delete_dir(self.subdirectory)
        return final_file
