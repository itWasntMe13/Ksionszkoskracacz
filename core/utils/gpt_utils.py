from importlib.metadata import version, PackageNotFoundError


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


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Zlicza liczbę tokenów w tekście.
    :param text:
    :param model: Model OpenAI, domyślnie "gpt-4"
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
