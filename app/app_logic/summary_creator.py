from app.app_logic import file_manager, api_manager, text_manager
from app.books.normalization import normalize_title
from core.config import *


def get_summary(title, _save_summary) -> str:
    # Tworzymy listę części streszczenia
    summary_parts_list = create_summary_parts_list(title)

    # Jeśli lista ma tylko jeden indeks, to znaczy, że całość książki zmieściła się w jednym zapytaniu, czyli nie trzeba łączyć streszczeń.
    if len(summary_parts_list) == 1:
        summary = summary_parts_list[0]

        # Jeśli save_summary == True, zapisujemy streszczenie
        if _save_summary:
            save_summary(title, summary)

        return summary_parts_list[0]
    else:
        summary = merge_summary(summary_parts_list)

        # Jeśli save_summary == True, zapisujemy streszczenie
        if _save_summary:
            save_summary(title, summary)

    return summary


def save_summary(title, summary):
    # Normalizujemy tytuł
    normalized_title = normalize_title(title)

    # Określamy ścieżkę do pliku
    summary_path = f"{GLOBAL_PATH}\\files\\ai\\summaries\\{normalized_title}.txt"

    # Zapisujemy streszczenie
    file_manager.save_file(summary_path, summary)
    print(f"Streszczenie zostało zapisane w pliku {summary_path}.")


def merge_summary(summary_parts_list) -> str:
    # Tworzymy stringa na streszczenie
    merged_summary = ""

    # Łączymy streszczenia w jeden tekst
    for summary in summary_parts_list:
        # Łączymy streszczenia w jeden tekst
        merged_summary += summary

    # Zwracamy połączone streszczenie
    return merged_summary


# Funkcja tworząca listę części streszczeń
def create_summary_parts_list(title) -> list:
    # Normalizujemy tytuł
    normalized_title = normalize_title(title)

    # Określamy ścieżkę do książki
    book_path = (
        f"{GLOBAL_PATH}\\files\\wolne_lektury\\books\\txt\\{normalized_title}.txt"
    )

    # Wczytujemy książkę
    book_content = file_manager.load_file(book_path)

    # Dzielimy tekst na fragmenty
    list_of_fragments = text_manager.split_text(book_content, 15000)

    # Określamy instrukcje dla GPT
    summary_system_role = (
        "Utwórz streszczenie poniższego fragmentu tekstu."
        "Odpowiedź ma zawierać jedynie streszczenie, żadnych wstępów lub komentarzy tak, by móc ten fragment połączyć z poprzednim i następnym."
        "\nTekst:"
    )

    # Tworzymy listę na części streszczenia
    summaries = []

    # Dla każdego fragmentu tworzymy obiekt zapytania do API
    for fragment in list_of_fragments:
        # Łączymy instrukcje dla API z aktualnie przetwarzanym fragmentem tekstu
        prompt = f"{summary_system_role}\n{fragment}"

        # Tworzymy obiekt
        gpt_summary_obj = api_manager.GPTPrompt(
            prompt, MY_API_KEY, DEFAULT_MODEL, TOKEN_LIMIT
        )

        # Wysyłamy zapytanie do API z włączonym zapisem informacji
        gpt_summary_obj.get_gpt(prompt, save_info=False, save_response=False)

        # Dodajemy odpowiedź do listy streszczeń
        summaries.append(gpt_summary_obj.response)

    # Zwracam listę części streszczenia
    return summaries
