from .utils import get_next_available_path
from typing import Tuple, List
import os
import shutil
import requests
import logging
import hashlib

logger = logging.getLogger(__name__)


class File:
    def __init__(self,
                 path: str,
                 extensions: List[str] = None) -> None:
        self.path = path
        self.extensions = extensions or []
        self.validate_extensions()
        self.data = self.load()

    def save(self) -> None:
        os.makedirs(self.dir, exist_ok=True)
        with open(self.path, 'wb') as f:
            f.write(self.data)
        logger.debug(f'File saved: {self.path}')

    def load(self) -> bytes:
        self.validate_file()
        with open(self.path, 'rb') as f:
            data = f.read()
        logger.debug(f"Loaded file: {self.path}")
        return data

    def replace_with(self, source_file: 'File') -> None:
        if self.exists():
            self.delete()
        shutil.move(source_file.path, self.path)
        self.data = self.load()
        logger.debug(f"Replaced {self.path} with {source_file.path}")

    def delete(self) -> None:
        os.remove(self.path)
        logger.debug(f"Deleted file: {self.path}")

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def validate_extensions(self) -> bool:
        if self.extensions and not any(self.path.endswith(ext) for ext in self.extensions):
            raise ValueError(f"File {self.path} does not have any of the required extensions {self.extensions}.")
        return True

    def validate_file(self) -> bool:
        if not self.exists():
            raise FileNotFoundError(f"File {self.path} does not exist.")
        if not os.path.isfile(self.path):
            raise ValueError(f"Path {self.path} is not a file.")
        if not self.validate_extensions():
            raise ValueError(f"File {self.path} does not have any of the required extensions {self.extensions}.")
        return True

    @property
    def dir(self) -> str:
        dir, _name, _ext = self.split_name()
        return dir

    @property
    def name(self) -> str:
        _dir, name, _ext = self.split_name()
        return name

    @property
    def ext(self) -> str:
        _dir, _name, ext = self.split_name()
        return ext

    def split_name(self) -> Tuple[str, str, str]:
        dir, name = os.path.split(self.path)
        name, ext = os.path.splitext(name)
        return dir, name, ext

    def copy(self, destination: str = None) -> 'File':
        if not destination:
            destination = self.path.replace(self.ext, f"_copy{self.ext}")

        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy(self.path, destination)
        logger.debug(f"Copied file from {self.path} to {destination}")

        # Return a new instance of the same class with the updated path
        return type(self)(path=destination)

    @property
    def hash(self):
        hash_obj = hashlib.sha256()
        with open(self.path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()


def download_file(url: str, destination: str) -> str:
    destination = get_next_available_path(destination)
    response = requests.get(url)
    response.raise_for_status()
    with open(destination, 'wb') as handler:
        handler.write(response.content)
    return destination
