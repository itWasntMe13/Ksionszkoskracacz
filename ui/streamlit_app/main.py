import sys
import os
import streamlit as st
from pathlib import Path
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from ui.streamlit_app import choose_a_book_view, admin_view, summary_generator_view, helpers, character_list_view
from ui.config.providers import AiProviders

# Ustawiamy logo i favicon
favicon = Image.open('ui/img/favicon.ico')
if favicon:
    st.set_page_config(page_title="Ksionszkoskracacz", page_icon=favicon, layout="wide")
else:
    st.set_page_config(page_title="Ksionszkoskracacz", layout="wide")

logo_path = Path('ui/img/main_logo.png')
if logo_path.exists():
    st.sidebar.image(logo_path, use_container_width=True)

# Jeśli wybrano książkę to wyświetl co to za książka na sidebarze
if "selected_book" in st.session_state and st.session_state.selected_book:
    book = st.session_state.selected_book
    st.sidebar.info(f"Aktywna książka:\n## **{book.title}**\n\n**{book.author}**")

# Sidebar – część nawigacji po aplikacji
st.sidebar.title("Nawigacja")
page = st.sidebar.radio(
    "Wybierz tryb:", ["# Wybór książki", "# Generator streszczeń", "#  Lista bohaterów", "# Admin"]
)

st.sidebar.divider()

# Sidebar - część wyboru AI
selected_provider = st.sidebar.selectbox(
    "Silnik AI:", options=[p.value for p in AiProviders]
)
# Wywołanie inicjalizatora AiService
helpers.init_ai_service(selected_provider)

# Widoki
if page == "# Wybór książki":
    choose_a_book_view.show()
elif page == "# Generator streszczeń":
    summary_generator_view.show()
elif page == "# Lista bohaterów":
    character_list_view.show()
elif page == "# Admin":
    admin_view.show()
