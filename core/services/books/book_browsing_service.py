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
        Wyszukuje książki na podstawie wielu atrybutów (np. title + author). Porzucona na rzecz filter_books która jest bardziej niezawodna.
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

    @staticmethod
    def filter_books(
        books: list[BookIndex], author_q: str = "", title_q: str = ""
    ) -> list[BookIndex]:
        filtered = books

        if author_q:
            filtered = [
                b for b in filtered if author_q.casefold() in b.author.casefold()
            ]

        if title_q:
            filtered = [b for b in filtered if title_q.casefold() in b.title.casefold()]

        return filtered
