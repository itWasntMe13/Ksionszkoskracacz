import streamlit as st
import sys
import os

from narwhals.selectors import matches
from streamlit import title, button

from core.models.books.book import Book

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from core.config.config import BOOKS_DIR
from core.utils.common_utils import load_json_file
from core.services.books.book_index_service import BookIndexService
from core.services.books.book_browsing_service import BookBrowsingService
from core.services.books.book_detail_service import BookDetailService
from core.services.books.book_service import BookService


def show():
    # Tytuł aplikacji
    st.title("📚 Przeglądarka Wolnych Lektur")
    st.markdown("Twoje centrum lektur i wiedzy – powered by 🧠 & ☕")

    # Pobieramy indeks książek z pamięci sesji
    book_index_list = BookIndexService.load_books_index_json()

    title_query = st.text_input("**Tytuł**", "")  # Query do wyszukiwania tytułów
    author_query = st.text_input("**Autor**", "")  # Query do wyszukiwania autorów
    # Usuwamy białe znaki z początku i końca
    title_query = title_query.strip()
    author_query = author_query.strip()

    if title_query or author_query:
        if title_query and author_query:
            matches = BookBrowsingService.search_books_by_attrs(
                book_index_list, ["title", "author"], f"{title_query} – {author_query}"
            )
        elif title_query and not author_query:
            matches = BookBrowsingService.search_books_by_attrs(
                book_index_list, ["title"], title_query
            )
        elif author_query and not title_query:
            matches = BookBrowsingService.search_books_by_attrs(
                book_index_list, ["author"], author_query
            )

        if matches:
            options = [f"{book.title} - {book.author}" for book in matches]
            selected = st.selectbox("Wybierz książkę:", options)

            if selected:
                selected_index = options.index(selected)
                chosen_book = matches[selected_index]

                # Pobieramy detale książki, która została wybrana
                BookDetailService.download_book_details_json(chosen_book)
                book_detail = BookDetailService.load_book_details_json(chosen_book)

                st.markdown(f"### 📘 {book_detail.title}")
                st.markdown(f"👤 **Autor:** {book_detail.author}")
                st.markdown(f"📚 **Gatunek:** {book_detail.genre}")
                st.markdown(f"📜 **Epoka:** {book_detail.epoch}")
                st.markdown(f"🧾 **Rodzaj:** {book_detail.kind}")

                if not book_detail.txt_url:
                    st.error(
                        "🚫 Książka niedostępna w formacie TXT. Spróbuj później lub wybierz inną."
                    )
                else:
                    # Ścieżka do pliku JSON z obiektem Book
                    book_path = BOOKS_DIR / f"{book_detail.slug}.json"
                    book_content = None

                    # Jeśli książka już istnieje lokalnie
                    if book_path.exists():
                        st.info("Książka już pobrana — wczytuję z lokalnego pliku.")
                        book_dict = load_json_file(book_path)
                        st.session_state["selected_book"] = Book.from_dict(book_dict)
                        book_content = book_dict.get("content")

                    # Pobieranie książki
                    if st.button("⬇️ Pobierz książkę"):
                        book_obj = BookService.create_book_object(
                            book_detail, save=True
                        )
                        st.session_state["selected_book"] = book_obj
                        book_content = book_obj.content
                        st.success("✅ Książka została pobrana i zapisana.")

                    # Wyświetlanie treści książki, jeśli jest dostępna
                    if book_content:
                        st.markdown("---")
                        st.subheader("📖 Treść książki")
                        st.text_area("📝 Podgląd treści:", book_content, height=500)

    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #1c1c1e;
            color: #ccc;
            text-align: center;
            padding: 10px;
            font-size: 0.875rem;
            box-shadow: 0 -1px 3px rgba(0,0,0,0.4);
        }

        .footer a {
            color: #4ba3fa;
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }
        </style>

        <div class="footer">
            📚 Wszystkie książki pochodzą z serwisu <a href="https://wolnelektury.pl" target="_blank">Wolne Lektury</a> • © Michał Rakoczy
        </div>
        """,
        unsafe_allow_html=True,
    )
