import openai
import tiktoken
import requests
import PIL.Image
from io import BytesIO
from core.config.config import OPENAI_VERSION
from app.app_logic.file_manager import append_file, save_image


# Klasa do obsługi API dla GPT-3.5
class GPTPrompt:
    def __init__(self, prompt, api_key, model, token_limit):
        openai.api_key = api_key  # Ustawienie klucza API dla openai
        self.model = model  # Model AI, w projekcie używamy GPT-3.5 Turbo
        self.token_limit = token_limit  # Limit tokenów na odpowiedź
        self.prompt = prompt  # Zapytanie do API
        self.response = None  # Odpowiedź z API
        self.cost = None  # Przybliżony koszt zapytania i odpowiedzi
        self.input_tokens = self.count_tokens(
            prompt
        )  # Liczbę tokenów w zapytaniu można wyliczyć od razu
        self.output_tokens = None  # Liczba tokenów w odpowiedzi

    # Metoda wyświetlająca informacje o obiekcie
    def __str__(self):
        return (
            f"Prompt: {self.prompt}\n"
            f"Response: {self.response}\n"
            f"Cost: {self.cost}\n"
            f"Input tokens: {self.input_tokens}\n"
            f"Output tokens: {self.output_tokens}"
        )

    # Funkcja odbierająca odpowiedź i generująca informacje o zapytaniu
    def get_gpt(
        self, system_role, save_info, save_response, save_debug=False, save_to=None
    ):
        self.response = self.__send_prompt(system_role, save_debug)
        # self.output_tokens = self.count_tokens(self.response)
        # self.cost = self.__cost()
        # Zapisz informacje o zapytaniu/odpowiedzi do pliku, jeśli save_info = True
        self.__save_response_info(save_to) if save_info else None
        # Zapisz odpowiedź do pliku, jeśli save_response = True
        self.__save_response(save_to) if save_response else None

    # Funkcja zliczająca tokeny w tekście
    def count_tokens(self, text):
        print(f"Using model: {self.model}")
        # Pobranie kodowania dla modelu
        encoding = tiktoken.encoding_for_model(self.model)
        return len(encoding.encode(text))

    # Funkcja zapisująca do pliku tylko odpowiedź
    def __save_response(self, save_to):
        content = f"Response: {self.response}"
        # save_to = f"{save_to}/responses_only.txt"
        append_file(save_to, content)
        print(f"Zapisano odpowiedź w {save_to}")

    # Funkcja zapisująca do pliku pełne informacje o zapytaniu i odpowiedzi
    def __save_response_info(self, save_to):
        content = (
            f"Response: {self.response}\n"
            f"Cost: {self.cost}\n"
            f"Input tokens: {self.input_tokens}\n"
            f"Output tokens: {self.output_tokens}"
        )
        save_to = f"{save_to}/responses_full.txt"
        append_file(save_to, content)
        print(f"Zapisano informacje zapytania/odpowiedzi w {save_to}")

    # Funkcja do wysłania zapytania do API
    def __send_prompt(self, system_role, save_debug, save_debug_to=None):
        try:
            print(f"Wysyłanie zapytania do {self.model}...")
            # Jeśli wersja openai jest starsza niż 1.0.0
            if OPENAI_VERSION < "1.0.0":
                # Dla wersji 1.0.0 i nowszych
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_role},
                        {"role": "user", "content": self.prompt},
                    ],
                    max_tokens=1000,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )
            else:
                response = openai.completions.create(
                    model=self.model,
                    prompt=self.prompt,
                    max_tokens=1000,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )

            if response:  # Czy odpowiedź istnieje
                print("Odebrano odpowiedź...")

            # Zapisanie informacji debugowania
            if save_debug:
                content = f"Prompt: {self.prompt}\nResponse: {response}"
                append_file(f"{save_debug_to}/log.txt", content)
                print(f"Zapisano dane debug w {save_debug_to}/log.txt")

            response = response["choices"][0]["message"]["content"].strip()
            return response
        except Exception as e:
            return f"An error occurred while sending a prompt to GPT-3.5 Turbo: {e}"

    # Funkcja obliczająca łączny koszt zapytania i odpowiedzi
    def __cost(self):
        cost_per_1000_tokens_prompt = 0.0015
        cost_per_1000_tokens_response = 0.002

        prompt_tokens = self.count_tokens(self.prompt)
        response_tokens = self.count_tokens(self.response)

        # Obliczenie kosztu na podstawie ilości tokenów * koszt za 1000 tokenów
        prompt_cost = (prompt_tokens / 1000) * cost_per_1000_tokens_prompt
        response_cost = (response_tokens / 1000) * cost_per_1000_tokens_response
        return prompt_cost + response_cost


# Klasa do obsługi API dla DALL-E
class DALLEPrompt:
    def __init__(
        self,
        prompt,
        api_key,
        model,
        size,
        n,
        save_info_to,
        save_img,
        save_info,
        save_url,
        save_prompt,
    ):
        openai.api_key = api_key  # Ustawienie klucza API dla openai
        self.model = model  # Model AI, w projekcie używamy DALL-E 2.0
        self.prompt = prompt  # Zapytanie do API
        self.size = size  # Rozmiar obrazka
        self.n = n  # Ilość obrazków do wygenerowania
        self.response = None  # Odpowiedź z API (URL obrazka)
        self.URL = None  # URL obrazka
        self.cost = self.__cost()  # Przybliżony koszt zapytania i odpowiedzi
        self.img = None  # Obrazek z odpowiedzi
        self.save_info_to = (
            save_info_to  # Ścieżka do zapisu informacji o zapytaniu i odpowiedzi
        )
        self.save_img = save_img  # Czy zapisać obrazek
        self.save_info = save_info  # Czy zapisać informacje
        self.save_url = save_url  # Czy zapisać URL
        self.save_prompt = save_prompt  # Czy zapisać prompt

    # Metoda wyświetlająca informacje o obiekcie
    def __str__(self):
        return f"Prompt: {self.prompt}\n" f"Cost: {self.cost}\n" f"URL: {self.URL}\n"

    def get_dalle(self):
        self.response = self.__send_prompt()
        self.URL = self.__extract_response_url()
        self.img = self.__download_img()
        if self.save_info:
            self.__save_response_info(self.save_info_to, self.save_prompt)
        # if self.save_url:
        #    self.__save_response_url(self.save_info_to)
        if self.save_img:
            self.__save_img()

    # Funkcja do wyświetlania odpowiedzi (obrazka) w Pythonie za pomocą PIL
    def show_response_img(self):
        self.img.show()

    # Funkcja do wysłania zapytania do API
    def __send_prompt(self, save_debug_to) -> dict:
        try:
            print(f"Wysyłanie zapytania do {self.model}...")
            response = openai.Image.create(
                prompt=self.prompt,
                n=1,
                size=self.size,
            )
            if response:
                print("Odebrano odpowiedź...")

            # Jeśli odpowiedź nie jest słownikiem to zwróć komunikat-przydatne do debugowania
            if not isinstance(response, dict):
                print("Response is not a dictionary")

            # Zapisanie informacji debugowania
            content = f"Prompt: {self.prompt}\nResponse: {response}"
            append_file(f"{save_debug_to}/log.txt", content)
            print(f"Zapisano dane debug w {save_debug_to}/log.txt")

            return response
        except Exception as e:
            return {"error": f"An error occurred while sending a prompt to DALL-E: {e}"}

    # Funkcja do wyciągnięcia URL z odpowiedzi
    def __extract_response_url(self):
        # Sprawdzamy, czy odpowiedź jest poprawna
        if isinstance(self.response, dict):
            try:
                # Zwracamy pierwszy URL z listy "data"
                return self.response["data"][0]["url"]
            except (KeyError, IndexError):
                return "URL not found in the response"
        else:
            return "Invalid response format"

    # Funkcja pobierająca images z odpowiedzi
    def __download_img(self) -> PIL.Image:
        # print("URL: " + self.URL) # Do debugowania-wyświetla URL z pliku
        print("Pobieranie obrazka...")  # Komunikat dla użytkownika
        response = requests.get(self.URL)
        # print(response)  # Do debugowania - przy poprawnym działaniu zwraca <Response [200]>
        response.raise_for_status()  # Sprawdza, czy odpowiedź HTTP jest błędem
        img = PIL.Image.open(BytesIO(response.content))
        print("Udało się pobrać obrazek.")  # Do debugowania
        return img  # Zwracamy pobrany obraz

    # Funkcja zapisująca image z odpowiedzi do pliku
    def __save_img(self) -> None:
        img = self.img

        if img:
            print("Zapisywanie obrazka przez file_manager...")  # Do debugowania
            save_image(img)  # Zapisz obraz do pliku

    # Funkcja zapisująca URL odpowiedzi do pliku
    def __save_response_url(self, save_info_to):
        # Dopisanie URL do pliku
        content = f"Response URL: {self.response}"
        save_info_to = f"{save_info_to}/responses_url.txt"
        append_file(save_info_to, content)

    # Funkcja zapisująca informacje o zapytaniu i odpowiedzi do pliku
    def __save_response_info(self, save_info_to):
        # Dopisanie informacji do pliku
        content = (
            f"Prompt: {self.prompt}\n"
            f"Response URL: {self.response}\n"
            f"Cost: {self.cost}\n"
        )
        save_info_to = f"{save_info_to}_info.txt"
        append_file(save_info_to, content)

    # Funkcja obliczająca koszt zapytania
    def __cost(self):
        # Koszt zależy od rozmiaru obrazka i użytego modelu
        if self.model == "dall-e-2.0":
            if self.size == "256":
                return 0.016
            elif self.size == "512":
                return 0.018
            elif self.size == "1024":
                return 0.02
            else:
                return 0.01
        elif self.model == "dall-e-3":
            if self.size == "1024":
                return 0.01
