import openai

from core.config.gpt import GptConfig
from core.services.gpt.gpt_config_service import GptConfigService
from core.utils.gpt_utils import count_tokens


class GptService:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.gpt_config = GptConfigService.load_config()

    @staticmethod
    def is_summarizable(text: str, gpt_config: GptConfig) -> bool:
        """
        Sprawdza, czy książka jest wystarczająco krótka do podsumowania.
        :param text:
        :param gpt_config:
        :param book: Obiekt książki.
        :return: True, jeśli książka jest wystarczająco krótka do podsumowania, False w przeciwnym razie.
        """
        token_count = count_tokens(text)  # Liczymy tokeny w treści książki

        if token_count < gpt_config.prompt_percentage * gpt_config.max_tokens:
            return True
        else:
            return False

    def summarize_text(
        self, gpt_config: GptConfig, text: str, system_prompt: str = None
    ) -> str:
        prompt = system_prompt or "Stwórz streszczenie edukacyjne załączonego tekstu."
        model = gpt_config.model

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
