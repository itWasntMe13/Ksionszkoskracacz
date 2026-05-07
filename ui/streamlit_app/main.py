import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from ui.streamlit_app import choose_a_book_view, admin_view, smart_view, helpers
from ui.config.providers import AiProviders

# Jeśli wybrano książkę to wyświetl co to za książka na sidebarze
if "selected_book" in st.session_state and st.session_state.selected_book:
    book = st.session_state.selected_book
    st.sidebar.success(f"## **{book.title}**\n\n**{book.author}**")


# Sidebar – część nawigacji po aplikacji
st.sidebar.title("Nawigacja")
page = st.sidebar.radio(
    "Wybierz tryb:", ["📖 Wybór książki", "⚙️ Asystent AI", "🛠️ Admin"]
)

st.sidebar.divider()

# Sidebar - część wyboru AI
selected_provider = st.sidebar.selectbox(
    "Silnik AI:", options=[p.value for p in AiProviders]
)
# Wywołanie inicjalizatora AiService
helpers.init_ai_service(selected_provider)

# Widoki
if page == "📖 Wybór książki":
    choose_a_book_view.show()
elif page == "⚙️ Asystent AI":
    smart_view.show()
elif page == "🛠️ Admin":
    admin_view.show()
