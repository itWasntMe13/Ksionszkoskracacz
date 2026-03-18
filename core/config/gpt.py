# Ogólne
from dataclasses import dataclass
from core.config.config import PROJECT_ROOT
from core.config.enums import GptModelInfo
from core.utils.common_utils import load_json_file
from core.utils.gpt_utils import check_openai_version

OPENAI_VERSION = check_openai_version()  # Wersja zainstalowanej biblioteki OpenAI

PROMPTS = load_json_file(PROJECT_ROOT / "core/config/prompts.json")


@dataclass
class GptConfig:
    model: str  # Domyślny model
    max_tokens: int = (
        10000  # RPM czyli requests per minute dla gpt-4o-mini to 10 000 tokenów.
    )
    temperature: float = 0.7
    output_percentage: float = (
        0.2  # np.: 0,2 * 128 000 = 25 600 tokenów model może wydać na output dla gpt-4o-mini.
    )
    prompt_percentage: float = (
        0.8  # np.: 0,8 * 128 000 = 102 400 tokenów model może wydać na input dla gpt-4o-mini.
    )

    def to_dict(self):
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "output_percentage": self.output_percentage,
            "prompt_percentage": self.prompt_percentage,
        }

    @staticmethod
    def from_dict(config_dict):
        return GptConfig(
            model=config_dict.get("model"),
            max_tokens=config_dict.get("max_tokens", 128000),
            temperature=config_dict.get("temperature", 0.7),
            output_percentage=config_dict.get("output_percentage", 0.2),
            prompt_percentage=config_dict.get("prompt_percentage", 0.8),
        )

    def validate(self):
        assert 0 <= self.temperature <= 1, "Temperature musi być w zakresie 0-1"
        assert 0 < self.output_percentage <= 1, "Max output % musi być między 0-1"
        assert 0 < self.prompt_percentage <= 1, "Prompt % musi być między 0-1"
        assert (
            self.output_percentage + self.prompt_percentage == 1
        ), "Suma max output % i prompt % musi wynosić 1"
