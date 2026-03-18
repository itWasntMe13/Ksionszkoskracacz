import os
from pathlib import Path
from pandas.io.common import file_exists

from core.config.config import (
    BOOKS_DIR,
    BOOK_DETAILS_DIR,
    REQUIRED_DIRS,
    BOOKS_INDEX_RAW_PATH,
    BOOKS_INDEX_PATH,
)
from core.services.books import book_index_raw_service, book_index_service


class MaintenanceService:
    """
    Funkcje pomocnicze pozwalające na resetowanie stanu aplikacji z poziomu jej interfejsu.
    """

    @staticmethod
    def clear_books_dir(directory=BOOKS_DIR):
        """
        Usuwa wszystkie książki z katalogu BOOKS_DIR.
        """
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    @staticmethod
    def clear_books_details_dir(directory=BOOK_DETAILS_DIR):
        """
        Usuwa wszystkie pliki z katalogu BOOK_DETAILS_DIR.
        """
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    @staticmethod
    def build_environment():
        """
        Tworzy strukturę plików na dane wejściowe i wyjściowe.
        :return:
        """
        for directory in REQUIRED_DIRS:
            try:
                Path(directory).mkdir(parents=True, exist_ok=True)
                print(f"Utworzono katalog: {directory}")
            except Exception as e:
                print(f"Nie udało się utworzyć katalogu: {directory}. Błąd: {e}")

    @staticmethod
    def create_book_indexes(force_update=False):
        """
        Tworzy indeksy książek.
        :param force_update:
        :return:
        """
        if force_update or not file_exists(BOOKS_INDEX_RAW_PATH):
            book_index_raw_service.BookIndexRawService.download_books_index_raw_json()

        if force_update or not file_exists(BOOKS_INDEX_PATH):
            book_index_service.BookIndexService.create_books_index_json()
