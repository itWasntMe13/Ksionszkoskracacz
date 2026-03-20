from importlib.metadata import version, PackageNotFoundError

from core.config.unified_ai_config import UnifiedAiConfig


def check_openai_version() -> str:
    """
    Sprawdza wersję zainstalowanej biblioteki openai.
    :return:
    """
    try:
        version_openai = version("openai")
        print(f"Zainstalowana wersja openai: {version_openai}")
        return version_openai
    except PackageNotFoundError:
        print("Biblioteka openai nie jest zainstalowana.")
        return None

def count_gpt_tokens(text: str, model: str) -> int:
    """
    Zlicza liczbę tokenów w tekście.
    :param text:
    :param model: Model AI
    :return:
    """
    try:
        import tiktoken

        encoding = tiktoken.encoding_for_model(model)
        tokens = len(encoding.encode(text))
        return tokens
    except ImportError:
        print("Biblioteka tiktoken nie jest zainstalowana.")
        return None
