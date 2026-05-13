import openai
import logging
from core.config.unified_ai_config import UnifiedAiConfig, PROMPTS
from core.utils.ai_utils import count_gpt_tokens

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )

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
