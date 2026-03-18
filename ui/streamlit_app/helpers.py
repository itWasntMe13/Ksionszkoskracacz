import streamlit as st
from core.models.books.book import Book


def set_selected_book(book: Book):
    st.session_state.selected_book = book


def get_selected_book() -> Optional[Book]:
    return st.session_state.get("selected_book", None)


def clear_selected_book():
    if "selected_book" in st.session_state:
        del st.session_state["selected_book"]
