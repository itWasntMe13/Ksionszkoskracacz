import streamlit as st
import sys
import os
from core.models.books.book import Book
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "..")))

from core.config.config import BOOKS_DIR, BOOK_DETAILS_DIR
from core.utils.common_utils import load_json_file
from core.services.books.book_index_service import BookIndexService
from core.services.books.book_browsing_service import BookBrowsingService
from core.services.books.book_detail_service import BookDetailService
from core.services.books.book_service import BookService

st.title("Wybierz książkę")

# Pobieramy indeks książek
book_index_list = BookIndexService.load_books_index_json()

# Inicjalizacja stanów sesji
if "matched_books" not in st.session_state:
    st.session_state.matched_books = []
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
    st.session_state.matched_books = BookBrowsingService.filter_books(
        book_index_list, author_input, title_input
    )

    if not st.session_state.matched_books:
        st.warning("Brak dopasowań.")

if st.session_state.matched_books:
    options = [f"{b.author} - {b.title}" for b in st.session_state.matched_books]

    # Odzyskujemy indeks książki
    saved_index = st.session_state.get("saved_book_index", 0)
    saved_index = saved_index if saved_index < len(options) else 0

    selected = st.selectbox(
        "Wybierz książkę:", options, index=saved_index
    )

    if selected:
        # Zapis wyboru, który przetrwa skakanie po widokach
        st.session_state["saved_book_index"] = options.index(selected)
        chosen_book_index = st.session_state.matched_books[st.session_state["saved_book_index"]]

        # Jeśli istnieje wczytujemy detale, jeśli nie to pobieramy detale książki.
        book_details_path = Path(BOOK_DETAILS_DIR) / f"{chosen_book_index.slug}.json"
        if book_details_path.exists():
            try:
                book_detail = BookDetailService.load_book_details_json(chosen_book_index)
            except Exception as e:
                print(f"Wystąpił błąd podczas wczytywania książki.")
        else:
            BookDetailService.download_book_details_json(chosen_book_index)
            book_detail = BookDetailService.load_book_details_json(chosen_book_index)

        st.markdown(f"### **{book_detail.title}**")
        st.markdown(f"**Autor:** {book_detail.author}")
        st.markdown(f"**Gatunek:** {book_detail.genre} **Epoka:** {book_detail.epoch} **Rodzaj:** {book_detail.kind}")

        if not book_detail.txt_url:
            st.error("Książka niedostępna w formacie TXT.")
        else:
            # Ścieżka do pliku JSON z obiektem Book
            book_path = BOOKS_DIR / f"{book_detail.slug}.json"
            book_content = None

            # Scenariusz A: Książka już pobrana
            if book_path.exists():
                st.info("Książka już pobrana - możesz ją przejrzeć lub ustawić jako aktywną.")
                book_dict = load_json_file(book_path)

                # TYLKO PODGLĄD - nie dotykamy st.session_state.selected_book!
                preview_book = Book.from_dict(book_dict)
                book_content = book_dict.get("content")

                # PRZYCISK ZATWIERDZENIA KONTEKSTU
                if st.button("Ustaw jako aktywną książkę"):
                    st.session_state.selected_book = preview_book
                    st.rerun()  # Odświeżenie UI żeby sidebar się zaktualizował

            # Scenariusz B: Książka jeszcze nie pobrana
            else:
                # Pobieranie książki (od razu ustawia jako aktywną po pobraniu)
                if st.button("⬇️ Pobierz i ustaw jako aktywną"):
                    with st.spinner("Pobieranie i analizowanie..."):
                        book_obj = BookService.create_book_object(book_detail, save=True)
                        st.session_state.selected_book = book_obj
                        book_content = book_obj.content
                        st.success("Książka została pobrana i zapisana.")
                        st.rerun()

            # Wyświetlanie treści książki, jeśli jest dostępna
            if book_content:
                st.markdown("---")
                st.subheader("Treść książki")
                st.text_area(label="Opracowanie:", value=book_content, height=500, label_visibility="collapsed")
