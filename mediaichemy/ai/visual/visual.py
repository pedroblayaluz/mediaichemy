from runware import Runware
import inspect
from functools import wraps
from abc import ABC, abstractmethod
from mediaichemy.file import HTTPDownloader
from mediaichemy.ai.ai import AIService
from dotenv import load_dotenv
load_dotenv()


def filter_params_for(target_func):
    """Decorator that filters kwargs to only include parameters that target_func accepts."""
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            sig = inspect.signature(target_func)

            filtered_kwargs = {
                k: v for k, v in kwargs.items()
                if k in sig.parameters
            }
            return await func(self, *args, **filtered_kwargs)
        return wrapper
    return decorator


class VisualAI(AIService, ABC):
    def __init__(self):
        self.runware_api_key = self.require_env_var("RUNWARE_API_KEY")

    @abstractmethod
    async def create(self,
                     prompt: str,
                     output_path: str,
                     **kwargs):
        pass

    async def _get_runware_client(self):
        runware_client = Runware(api_key=self.runware_api_key)
        await runware_client.connect()
        return runware_client

    def _set_defaults(self, **kwargs):
        kwargs.setdefault('includeCost', True)
        kwargs.setdefault('numberResults', 1)
        return kwargs

    @staticmethod
    def download(url, output_path):
        return HTTPDownloader().download(url, output_path)
