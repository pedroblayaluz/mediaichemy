from functools import wraps
from logging import getLogger
from mediaichemy.file import File
from abc import ABC, abstractmethod


class Editor(ABC):
    def __init__(self, file: File):
        self.file = file
        self.working_file = None
        self.validate_file()

    @property
    @abstractmethod
    def file_type(self):
        """Return the file type that this editor supports."""
        pass

    def validate_file(self):
        """Validate that the file is of the correct type."""
        if not isinstance(self.file, self.file_type):
            raise TypeError(f"This editor only works with {self.file_type.__name__} files,"
                            f" but got {type(self.file).__name__}")

    @staticmethod
    def edit_file(func):
        """
        Decorator that creates a working copy of the file before editing,
        replacing the original if the operation succeeds.
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            logger = getLogger()
            try:
                self.working_file = self.file.copy()
                func(self, *args, **kwargs)
                self._replace_with_working_copy()
                logger.debug(f"{self.__class__.__name__}:{func.__name__} succeeded")
                return self.file
            except Exception as e:
                self._cleanup_working_file()
                logger.error(f"{func.__name__} failed: {e}")
                raise
        return wrapper

    def _replace_with_working_copy(self):
        self.file.replace_with(self.working_file)
        self.working_file = None

    def _cleanup_working_file(self):
        if self.working_file and self.working_file.exists():
            self.working_file.delete()
