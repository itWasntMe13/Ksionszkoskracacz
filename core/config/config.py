from pathlib import Path

# Konfiguracja API
# Wolne Lektury
WL_API_BASE_URL = "https://wolnelektury.pl/api"
WL_API_BOOKS_URL = f"{WL_API_BASE_URL}/books"  # Adres API do pobierania książek

# Konfiguracja ścieżek projektu
# Główna ścieżka projektu (tam, gdzie main.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Katalog z wszystkimi plikami niewykonawczymi
FILES_DIR = PROJECT_ROOT / "files"

# Katalog z plikami statycznymi/konfiguracyjnymi. Tworzymy je podczas budowy środowiska, później traktujemy je jak bazę danych.
STATIC_DIR = FILES_DIR / "static"
BOOKS_INDEX_RAW_PATH = (
    STATIC_DIR / "books_index_raw.json"
)  # Surowy indeks książek pobrany z API
BOOKS_INDEX_PATH = (
    STATIC_DIR / "books_index.json"
)  # Indeks książek przetworzony do użytku w programie
BOOK_DETAILS_DIR = (
    STATIC_DIR / "book_details"
)  # Katalog z plikami JSON z danymi szczegółowymi książek

# Dane wejściowe
INPUT_DIR = FILES_DIR / "input"
BOOKS_DIR = INPUT_DIR / "books"

# Dane pośrednie. Dane, które są w trakcie przetwarzania, ale nie są jeszcze danymi wyjściowymi.
INTERMEDIATE_DIR = FILES_DIR / "intermediate"
SUMMARY_PARTS_DIR = (
    INTERMEDIATE_DIR / "summary_parts"
)  # Części streszczeń. Planowo będą to pliki temporary, które będą usuwane po zakończeniu przetwarzania.
GPT_RAW_DIR = INTERMEDIATE_DIR / "gpt_raw"  # Surowe JSON-y z API GPT
LOGS_DIR = INTERMEDIATE_DIR / "logs"  # Katalog z logami. Do debugu dla mnie.

# Dane wyjściowe. Dane, które są już przetworzone i gotowe do użycia.
OUTPUT_DIR = FILES_DIR / "output"
SUMMARY_TXT_DIR = (
    OUTPUT_DIR / "summaries_txt"
)  # Katalog z plikami tekstowymi ze streszczeniami

REQUIRED_DIRS = [
    FILES_DIR,
    STATIC_DIR,
    INPUT_DIR,
    BOOKS_DIR,
    INTERMEDIATE_DIR,
    SUMMARY_PARTS_DIR,
    GPT_RAW_DIR,
    LOGS_DIR,
    OUTPUT_DIR,
    SUMMARY_TXT_DIR,
    BOOK_DETAILS_DIR,
]

GPT_CONFIG_PATH = (
    PROJECT_ROOT / "core/config/gpt_config.json"
)  # Ścieżka do pliku konfiguracyjnego GPT
