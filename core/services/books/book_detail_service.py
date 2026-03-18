from core.config.config import BOOK_DETAILS_DIR
from core.models.books.book_detail import BookDetail
from core.utils.common_utils import load_json_file, save_json_file, json_request


class BookDetailService:
    @staticmethod
    def load_book_details_json(
        book_index, load_directory=BOOK_DETAILS_DIR
    ) -> BookDetail:
        """
        Wczytuje szczegóły książki z pliku JSON. Zwraca obiekt BookDetail.
        :param book_index: Obiekt BookIndex
        :param load_directory: Katalog, w którym znajdują się pliki JSON z danymi szczegółowymi książek
        :return: Obiekt BookIndex z danymi szczegółowymi
        """

        # Ścieżka do pliku JSON
        file_path = load_directory / f"{book_index.slug}.json"

        # Wczytujemy dane z pliku JSON
        book_detail = load_json_file(file_path)

        # Tworzymy obiekt BookDetail
        book_detail = BookDetail.from_json_dict(book_detail)
        return book_detail

    @staticmethod
    def download_book_details_json(book_index, save_dir=BOOK_DETAILS_DIR) -> None:
        """
        Pobiera szczegóły książki na podstawie pola href z obiektu BookIndex i zapisuje je do pliku JSON.
        :param book_index:
        :param save_dir:
        :return:
        """
        url = book_index.href  # book_index.href to URL do detali książki
        json_file = json_request(url)

        # Stworzenie obiektu klasy BookDetail
        book_detail = BookDetail.from_api_dict(json_file)

        # Dodajemy pola slug i kind z obiektu BookIndex
        book_detail.slug = book_index.slug
        book_detail.kind = book_index.kind

        # Ścieżka zapisu to slug z obiektu BookIndex
        save_path = save_dir / f"{book_index.slug}.json"

        # Serializacja obiektu BookDetail do JSON-a
        save_json_file(book_detail.to_dict(), save_path)
