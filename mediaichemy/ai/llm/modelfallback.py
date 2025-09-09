from functools import wraps
import asyncio
from pydantic_ai.exceptions import ModelHTTPError
import logging
logger = logging.getLogger(__name__)


class ModelFallback:
    @staticmethod
    def remove_duplicates(current_model, model_list):
        return [model for model in model_list if model != current_model]

    @staticmethod
    def get_models_to_try(instance):
        remaining_models = ModelFallback.remove_duplicates(instance.current_model, instance.model_list)
        return [instance.current_model] + remaining_models

    @staticmethod
    def should_retry(error):
        if isinstance(error, ModelHTTPError):
            return getattr(error, "status_code", None) in [400, 404, 429]
        return False

    @staticmethod
    def apply(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            models = ModelFallback.get_models_to_try(self)
            last_error = None

            for model in models:
                original_model = self.current_model
                try:
                    self.current_model = model
                    # Reconnect if the instance has a reconnect method
                    if hasattr(self, 'reconnect') and callable(self.reconnect):
                        self.reconnect()
                    result = await func(self, *args, **kwargs)
                    return result
                except Exception as error:
                    last_error = error
                    if ModelFallback.should_retry(error):
                        logger.warning(f"Model {model} failed with error: {error}. Retrying...")
                        await asyncio.sleep(1)
                        continue
                    else:
                        raise error
                finally:
                    self.current_model = original_model
            raise last_error or Exception("All models failed")
        return wrapper


def with_model_fallback(func):
    return ModelFallback.apply(func)
