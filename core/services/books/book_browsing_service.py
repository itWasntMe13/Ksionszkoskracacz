from aiohttp.web_routedef import static

from core.config.config import BOOKS_INDEX_PATH
from core.models.books.book_index import BookIndex
from core.services.books.book_index_service import BookIndexService

class BookBrowsingService:
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
