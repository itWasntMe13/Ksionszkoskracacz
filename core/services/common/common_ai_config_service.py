from core.config.config import GPT_CONFIG_PATH, GEMINI_CONFIG_PATH
from core.config.gemini_config import GeminiConfig
from core.config.gpt_config import GptConfig
from core.config.unified_ai_config import UnifiedAiConfig
from core.utils.common_utils import load_json_file


class AiConfigService:
    @staticmethod
    def load_config(provider: str = 'Gemini') -> UnifiedAiConfig:
        """
        Na podstawie wyboru modelu przez użytkownika, wczytuje jego konfigurację do klasy UnifiedAiConfig.
        :return: Obiekt klasy UnifiedAiConfig
        """
        if provider == 'Gemini':
            path = GEMINI_CONFIG_PATH
            g_config = GeminiConfig.from_dict(load_json_file(path))
            config = g_config.to_unified()
            return config
        elif provider == 'GPT':
            path = GPT_CONFIG_PATH
            g_config = GptConfig.from_dict(load_json_file(path))
            config = g_config.to_unified()
            return config
        else:
            raise ValueError(f"Nieznany provider: {provider}")
