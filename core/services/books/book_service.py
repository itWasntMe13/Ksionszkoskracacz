import os

from core.config.config import BOOKS_DIR
from core.config.gpt import GptConfig
from core.utils.common_utils import txt_request, save_json_file
from core.services.books.book_detail_service import BookDetail
from core.models.books.book import Book
from core.utils.gpt_utils import count_tokens


class BookService:
    @staticmethod
    def create_book_object(
        book_detail: BookDetail, save=False, save_dir_path=BOOKS_DIR
    ) -> Book:
        """
        Pobiera treść książki, a następnie tworzy obiekt Book na podstawie obiektu BookDetail. Umożliwia zapis.
        :param save_dir_path:
        :param book_detail:
        :param save: Czy zapisać książkę?
        :param save_dir_path: Ścieżka do katalogu, w którym zostanie zapisany plik JSON.
        :return:
        """
        book_content = BookService.download_book_txt(
            book_detail
        )  # Pobieramy treść książki

        # Tworzymy obiekt Book
        book = Book(
            slug=book_detail.slug,
            title=book_detail.title,
            content=book_content,
            author=book_detail.author,
            kind=book_detail.kind,
            epoch=book_detail.epoch,
            genre=book_detail.genre,
        )

        if save:
            BookService.save_book_as_json(
                book, save_dir_path
            )  # Zapisujemy książkę do pliku JSON

        return book

    @staticmethod
    def download_book_txt(book_detail) -> str:
        """
        Pobiera treść książki na podstawie obiektu BookDetail.
        :param book_detail:
        :param save_dir:
        :return: Treść książki w string-u.
        """
        if not book_detail.txt_url:
            print(f"Brak URL do książki {book_detail.title}")
            return None

        url = (
            book_detail.txt_url
        )  # book_detail.txt_url to URL do książki w formacie TXT
        book = txt_request(url)

        try:
            return book.decode("utf-8")  # Dekodowanie bajtów na string
        except UnicodeDecodeError as e:
            print(f"Błąd dekodowania książki {book_detail.title}: {e}")
            return None

    @staticmethod
    def save_book_as_json(book: Book, save_dir_path: str = BOOKS_DIR) -> None:
        """
        Zapisuje obiekt Book do pliku JSON.
        :param book: Obiekt książki do zapisania.
        :param save_dir_path: Ścieżka do katalogu, w którym zostanie zapisany plik JSON.
        """
        book_dict = book.to_dict()  # Zrzucamy obiekt do słownika
        save_file_path = os.path.join(
            save_dir_path, f"{book.slug}.json"
        )  # Tworzymy ścieżkę zapisu
        save_json_file(book_dict, save_file_path)

    @staticmethod
    def split_text_into_fragments(text: str, fragment_length: int = 3000) -> list[str]:
        """
        Dzieli tekst na fragmenty o zadanej długości (domyślnie 3000 znaków).

        :param text: Tekst wejściowy do podziału.
        :param fragment_length: Maksymalna długość pojedynczego fragmentu.
        :return: Lista fragmentów tekstu.
        """
        fragments = []
        text_length = len(text)
        for i in range(0, text_length, fragment_length):
            fragments.append(text[i : i + fragment_length])
        return fragments
