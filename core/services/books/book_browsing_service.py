
from core.models.books.book_index import BookIndex

class BookBrowsingService:
    """
    Zwraca indeks szukanej książki na podstawie danych autora i tytułu lub dowolnej jednej z tych danych.
    """
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
