import google.genai as genai
import logging

from click import prompt

from core.config.unified_ai_config import UnifiedAiConfig, PROMPTS

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )

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
            print()
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

    def generate_motifs_overview(self, text: str) -> str:
        prompt = (
            f"{PROMPTS['motifs_overview']['role']}\n"
            f"{PROMPTS['motifs_overview']['task']}\n"
            f"{PROMPTS['motifs_overview']['format']}\n\n"
            f"--- POCZĄTEK TREŚCI KSIĄŻKI ---\n"
            f"{text}\n"
            f"--- KONIEC TREŚCI KSIĄŻKI ---"
        )
        return self._generate(prompt)

    def generate_quiz(self, text: str) -> str:
        prompt = (
            f"{PROMPTS['quiz_generator']['role']}\n"
            f"{PROMPTS['quiz_generator']['task']}\n"
            f"{PROMPTS['quiz_generator']['format']}\n\n"
            f"--- POCZĄTEK TREŚCI KSIĄŻKI ---\n"
            f"{text}\n"
            f"--- KONIEC TREŚCI KSIĄŻKI ---"
        )
        return self._generate(prompt)