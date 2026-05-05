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

    # Inicjalizacja stanów sesji
    if "matches" not in st.session_state:
        st.session_state.matches = []
    if "selected_book" not in st.session_state:
        st.session_state.selected_book = None

    with st.form("search_form", clear_on_submit=False):
        col_a, col_t = st.columns(2)

        with col_a:
            author_input = st.text_input("Autor", key="author_search").strip()
        with col_t:
            title_input = st.text_input("Tytuł", key="title_search").strip()

        submit = st.form_submit_button("Filtruj")

    if submit:
        st.session_state.matches = BookBrowsingService.filter_books(book_index_list, author_input, title_input)

        if not st.session_state.matches:
            st.warning("Brak dopasowań.")

    if st.session_state.matches:
        options = [f"{b.author} - {b.title}" for b in st.session_state.matches]

        # Odzyskujemy indeks
        saved_index = st.session_state.get("saved_book_index", 0)
        saved_index = saved_index if saved_index < len(options) else 0

        selected = st.selectbox("Wybierz książkę:", options, index=saved_index, key="book_selector")

        if selected:
            # Zapis wyboru, który przetrwa skakanie po widokach
            st.session_state["saved_book_index"] = options.index(selected)

            selected_index = options.index(selected)
            chosen_book = st.session_state.matches[selected_index]

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
