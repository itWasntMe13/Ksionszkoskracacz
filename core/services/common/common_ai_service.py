import openai
import google.generativeai as genai

from core.config.unified_ai_config import UnifiedAiConfig, PROMPTS
from core.services.common.common_ai_config_service import AiConfigService
from core.utils.ai_utils import count_gpt_tokens

class CommonAiService:
    def __init__(self, provider: str):
        self.config = AiConfigService.load_config(provider)
        if self.config.provider == 'Gemini':
            self.ai_client = GeminiService(self.config)
        elif self.config.provider == 'GPT':
            self.ai_client = GptService(self.config)
        else:
            raise ValueError(f"Nieznany provider: {self.config.provider}")

    def count_tokens(self, text: str):
        return self.ai_client.count_tokens(text)

    def is_summarizable(self, text: str) -> bool:
        tokens = self.ai_client.count_tokens(text)
        return tokens <= self.config.total_context_limit

    def summarize_text(self, text: str) -> str:
        return self.ai_client.summarize_text(text)

class GeminiService:
    def __init__(self, unified_config: UnifiedAiConfig):
        self.config = unified_config
        genai.configure(api_key=self.config.api_key)
        self.model = genai.GenerativeModel(self.config.model_name)

    def count_tokens(self, text: str) -> int:
        try:
            # Używamy już skonfigurowanego modelu
            response = self.model.count_tokens(text)
            return response.total_tokens
        except Exception as e:
            print(f"Błąd zliczania Gemini: {e}")
            return 0

    def summarize_text(self, text: str) -> str:
        prompt = PROMPTS["summary"]["role"] + PROMPTS["summary"]["task"] + PROMPTS["summary"]["format"] + "TREŚĆ KSIĄŻKI:" + text # Konkatenujemy role, tekst, zadanie i format

        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": self.config.temperature,
                "max_output_tokens": self.config.max_tokens
            }
        )
        return response.text

class GptService:
    def __init__(self, unified_config: UnifiedAiConfig):
        self.config = unified_config

    def summarize_text(
        self, text: str, system_prompt: str = None
    ) -> str:
        prompt = system_prompt or "Stwórz streszczenie edukacyjne załączonego tekstu."
        model = self.config.model_name

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content

    def count_tokens(self, text: str):
        token_count = count_gpt_tokens(text, self.config.model_name)
        return token_count