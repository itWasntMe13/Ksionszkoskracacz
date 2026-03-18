from core.config.config import GPT_CONFIG_PATH
from core.config.gpt import GptConfig
from core.utils.common_utils import load_json_file


class GptConfigService:

    @staticmethod
    def load_config(path: str = GPT_CONFIG_PATH) -> GptConfig:
        """
        Wczytuje domyślną konfigurację GPT z pliku konfiguracyjnego.
        :return: Obiekt GPTConfig
        """
        config = load_json_file(path)
        config = GptConfig.from_dict(config)
        return config
