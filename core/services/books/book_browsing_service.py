from aiohttp.web_routedef import static

from core.config.config import BOOKS_INDEX_PATH
from core.models.books.book_index import BookIndex
from rapidfuzz import process, fuzz
from core.services.books.book_index_service import BookIndexService


class BookBrowsingService:
    @staticmethod
    def search_books_by_attrs(
        books_index_list: list[BookIndex], attrs: list[str], query: str, limit: int = 25
    ) -> list[BookIndex]:
        """
        Wyszukuje książki na podstawie wielu atrybutów (np. title + author).
        Łączy wartości atrybutów w jeden string i wykonuje fuzzy search.
        """
        # Tworzymy mapę: combined string -> BookIndex
        search_map = {
            " – ".join([getattr(book, attr) for attr in attrs]): book
            for book in books_index_list
        }

        # Wykonujemy fuzzy search na połączonych stringach
        matches = process.extract(
            query, list(search_map.keys()), scorer=fuzz.ratio, limit=limit
        )

        # Wyciągamy dopasowane książki z mapy
        matched_books = [search_map[match[0]] for match in matches]

        return matched_books
