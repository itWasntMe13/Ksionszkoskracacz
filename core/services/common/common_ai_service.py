import openai
import google.genai as genai

from core.config.unified_ai_config import UnifiedAiConfig, PROMPTS
from core.services.common.common_ai_config_service import AiConfigService
from core.utils.ai_utils import count_gpt_tokens


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

    def count_tokens(self, text: str):
        return self.ai_client.count_tokens(text)

    def is_summarizable(self, text: str) -> bool:
        tokens = self.ai_client.count_tokens(text)
        return tokens <= self.config.total_context_limit

    def summarize_text(self, text: str) -> str:
        return self.ai_client.summarize_text(text)

    def generate_characters_overview(self, text: str) -> str:
        return self.ai_client.generate_characters_overview(text)

class GeminiService:
    def __init__(self, unified_config: UnifiedAiConfig):
        self.config = unified_config
        self.client = genai.Client(api_key=self.config.api_key)
        self.model_id = self.config.model_name

    def count_tokens(self, text: str) -> int:
        try:
            response = self.client.models.count_tokens(
                model=self.model_id,
                contents=text
            )
            return response.total_tokens
        except Exception as e:
            print(f"Błąd wyliczania tokenów Gemini: {e}")
            return 0

    def _generate(self, prompt: str) -> str:
        """Metoda pomocnicza do generowania zapytań do Gemini żeby uprościć metody generujące"""
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=self.config.temperature)
            )
            return response.text.strip()
        except Exception as e:
            print(f"Błąd generowania Gemini: {e}")
            return "Wystąpił błąd podczas generowania treści."

    def summarize_text(self, text: str) -> str:
        prompt = (
            f"{PROMPTS['summary']['role']}\n"
            f"{PROMPTS['summary']['task']}\n"
            f"{PROMPTS['summary']['format']}\n\n"
            f"--- POCZĄTEK TREŚCI KSIĄŻKI ---\n"
            f"{text}\n"
            f"--- KONIEC TREŚCI KSIĄŻKI ---"
        )
        return self._generate(prompt)

    def generate_characters_overview(self, text: str) -> str:
        prompt = (
            f"{PROMPTS['characters_overview']['role']}\n"
            f"{PROMPTS['characters_overview']['task']}\n"
            f"{PROMPTS['characters_overview']['format']}\n\n"
            f"--- POCZĄTEK TREŚCI KSIĄŻKI ---\n"
            f"{text}\n"
            f"--- KONIEC TREŚCI KSIĄŻKI ---"
        )
        return self._generate(prompt)

class GptService:
    def __init__(self, unified_config: UnifiedAiConfig):
        self.config = unified_config

    def summarize_text(self, text: str, system_prompt: str = None) -> str:
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
