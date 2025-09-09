from pydantic.dataclasses import dataclass
from typing import Optional, List, Any
import requests


@dataclass
class Architecture:
    modality: Optional[str] = None
    input_modalities: Optional[List[str]] = None
    output_modalities: Optional[List[str]] = None
    tokenizer: Optional[str] = None
    instruct_type: Optional[str] = None


@dataclass
class Pricing:
    prompt: Optional[str] = None
    completion: Optional[str] = None
    request: Optional[str] = None
    image: Optional[str] = None
    web_search: Optional[str] = None
    internal_reasoning: Optional[str] = None
    input_cache_read: Optional[str] = None
    input_cache_write: Optional[str] = None
    audio: Optional[str] = None


@dataclass
class TopProvider:
    context_length: Optional[int] = None
    max_completion_tokens: Optional[int] = None
    is_moderated: Optional[bool] = None


@dataclass
class ModelInfo:
    id: Optional[str] = None
    canonical_slug: Optional[str] = None
    hugging_face_id: Optional[str] = None
    name: Optional[str] = None
    created: Optional[int] = None
    description: Optional[str] = None
    context_length: Optional[int] = None
    architecture: Optional[Architecture] = None
    pricing: Optional[Pricing] = None
    top_provider: Optional[TopProvider] = None
    per_request_limits: Optional[Any] = None
    supported_parameters: Optional[List[str]] = None


@dataclass
class ModelsResponse:
    data: Optional[List[ModelInfo]] = None


class OpenrouterModels:
    def __init__(self,
                 api_url: str = "https://openrouter.ai/api/v1/models"):
        self.api_url = api_url
        self.models: List[ModelInfo] = self.get_models()

    def get_models(self):
        response = requests.get(self.api_url)
        response.raise_for_status()
        return ModelsResponse(**response.json()).data

    @staticmethod
    def filter_tool_models(models: List[ModelInfo]) -> List[ModelInfo]:
        return [m for m in models if m.supported_parameters and "tools" in m.supported_parameters]

    @staticmethod
    def order_by_prompt_price(models: List[ModelInfo]) -> List[ModelInfo]:
        return sorted(models, key=lambda m: m.pricing.prompt if m.pricing else float("inf"))

    @staticmethod
    def extract_ids(models: List[ModelInfo]) -> List[str]:
        return [m.id for m in models if m.id]

    def get_cheapest_models(self) -> List[ModelInfo]:
        self.models = self.order_by_prompt_price(self.models)
        return self.extract_ids(self.models)

    def get_cheapest_tool_models(self) -> List[ModelInfo]:
        tool_models = self.filter_tool_models(self.models)
        tool_models = self.order_by_prompt_price(tool_models)
        return self.extract_ids(tool_models)
