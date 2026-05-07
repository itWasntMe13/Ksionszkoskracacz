import streamlit as st
from core.models.books.book import Book
from core.services.common.common_ai_service import CommonAiService
from ui.config.providers import AiProviders


def set_selected_book(book: Book):
    st.session_state.selected_book = book


# def get_selected_book() -> Optional[Book]:
#     return st.session_state.get("selected_book", None)


def clear_selected_book():
    if "selected_book" in st.session_state:
        del st.session_state["selected_book"]


def init_ai_service(selected_provider: str):
    # Jeśli instancja AiService nie istnieje w sesji lub jest niezgodna z wyborem użytkownika to budujemy nową
    if (
        "ai_service" not in st.session_state
        or st.session_state.ai_service.config.provider != selected_provider
    ):
        try:
            if selected_provider == AiProviders.GEMINI.value:
                api_key = st.secrets["GEMINI_API_KEY"]
            elif selected_provider == AiProviders.GPT.value:
                api_key = st.secrets["GPT_API_KEY"]
            else:
                raise ValueError(
                    f"Wybrany dostawca nie jest obsługiwany. {selected_provider}"
                )

            st.session_state.ai_service = CommonAiService(selected_provider, api_key)
        except KeyError as e:
            st.sidebar.error(f"Brak klucza API w ./streamlit/secrets.toml {e}")
            st.stop()
        except Exception as e:
            st.sidebar.error(f"Wystąpił błąd podczas inicjalizacji silnika AI: {e}")
