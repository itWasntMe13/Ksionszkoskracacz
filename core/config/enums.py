from enum import Enum


class GptModelInfo(Enum):
    GPT_4O_MINI = ("gpt-4o-mini", 128000)
    GPT_4O = ("gpt-4o", 128000)

    @property
    def model_name(self):
        return self.value[0]

    @property
    def max_tokens(self):
        return self.value[1]
