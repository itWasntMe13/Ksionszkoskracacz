import logging
from core.services.ai.gemini_service import GeminiService
from core.services.ai.gpt_service import GptService
from core.services.common.common_ai_config_service import AiConfigService

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )

class CommonAiService:
    def __init__(self, provider: str, api_key: str):
        # Tworzymy obiekt konfiguracyjny ogólny
        self.config = AiConfigService.load_config(provider)
        self.config.api_key = api_key

        # Na podstawie obiektu konfiguracyjnego tworzymy obiekt który będzie komunikował się z AI
        if self.config.provider == "Gemini":
            self.ai_client = GeminiService(self.config)
        elif self.config.provider == "GPT":
            self.ai_client = GptService(self.config)
        else:
            raise ValueError(f"Nieznany provider: {self.config.provider}")

    def clean_text(self, text: str) -> str:
        WL_FOOTER = "-----"

        if WL_FOOTER in text:
            return text.split(WL_FOOTER)[0].strip()
        return text

    def count_tokens(self, text: str):
        return self.ai_client.count_tokens(text)

    def is_summarizable(self, text: str) -> bool:
        tokens = self.ai_client.count_tokens(text)
        logging.info(f"Funkcja is_summarizable - tokens: {tokens}, total_context_limit: {self.config.total_context_limit}")
        return tokens <= self.config.total_context_limit

    def summarize_text(self, text: str) -> str:
        return self.ai_client.summarize_text(text)

    def generate_characters_overview(self, text: str) -> str:
        return self.ai_client.generate_characters_overview(text)

    def generate_motifs_overview(self, text: str) -> str:
        return self.ai_client.generate_motifs_overview(text)

    def generate_quiz(self, text: str) -> str:
        return self.ai_client.generate_quiz(text)
