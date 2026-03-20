from dataclasses import dataclass
from core.config.config import PROJECT_ROOT
from core.config.enums import GptModelInfo
from core.config.unified_ai_config import UnifiedAiConfig
from core.utils.common_utils import load_json_file
from core.utils.ai_utils import check_openai_version

@dataclass
class GptConfig:
    model: str
    api_key: str
    max_tokens: int
    total_context_limit: int
    temperature: float
    output_percentage: float
    prompt_percentage: float

    def to_unified(self):
        return UnifiedAiConfig(
            provider="GPT",
            model_name=self.model,
            api_key=self.api_key,
            max_tokens=self.max_tokens,
            total_context_limit=self.total_context_limit,
            temperature=self.temperature,
            output_percentage=self.output_percentage,
            prompt_percentage=self.prompt_percentage,
        )

    def to_dict(self):
        return {
            "model": self.model,
            "api_key": self.api_key,
            "max_tokens": self.max_tokens,
            "total_context_limit": self.total_context_limit,
            "temperature": self.temperature,
            "output_percentage": self.output_percentage,
            "prompt_percentage": self.prompt_percentage,
        }

    @staticmethod
    def from_dict(config_dict):
        return GptConfig(
            model=config_dict.get("model"),
            api_key=config_dict.get("api_key"),
            max_tokens=config_dict.get("max_tokens", 128000),
            total_context_limit=config_dict.get("total_context_limit", 1000000),
            temperature=config_dict.get("temperature", 0.7),
            output_percentage=config_dict.get("output_percentage", 0.2),
            prompt_percentage=config_dict.get("prompt_percentage", 0.8),
        )

    def validate(self):
        assert 0 <= self.temperature <= 1, "Temperature musi być w zakresie 0-1"
        assert 0 < self.output_percentage <= 1, "Max output % musi być między 0-1"
        assert 0 < self.prompt_percentage <= 1, "Prompt % musi być między 0-1"
        assert (
            self.output_percentage + self.prompt_percentage <= 1
        ), "Suma max output % i prompt % musi wynosić mniej niż 1."
