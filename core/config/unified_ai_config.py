from dataclasses import dataclass, field
from typing import Optional, Any, Dict
from core.config.config import PROJECT_ROOT
from core.utils.common_utils import load_json_file

PROMPTS = load_json_file(PROJECT_ROOT / "core/config/prompts.json")

@dataclass
class UnifiedAiConfig:
    """
    Klasa normalizująca nazewnictwo specyficznych modeli w celu uproszczenia logiki komunikacji z AI.
    """
    provider: str
    model_name: str
    api_key: str
    max_tokens: int
    total_context_limit: int
    temperature: float
    output_percentage: float
    prompt_percentage: float
