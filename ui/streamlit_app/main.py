import sys
import os
import streamlit as st
from pathlib import Path
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from ui.streamlit_app import helpers
from ui.streamlit_app.views import admin_view, choose_a_book_view, summary_generator_view, character_list_view, \
    quiz_generator_view
from ui.config.providers import AiProviders

# Ustawiamy logo i favicon
st.set_page_config(page_title="Ksionszkoskracacz", page_icon='ui/img/favicon.ico', layout="wide")
st.sidebar.image('ui/img/main_logo.png', use_container_width=True)

# Sidebar – część nawigacji po aplikacji
st.sidebar.title("Nawigacja")
page = st.sidebar.radio(
    "Wybierz tryb:", ["# Wybór książki", "# Generator streszczeń", "# Lista bohaterów", "# Quiz", "# Admin"]
)

st.sidebar.divider()
# Jeśli wybrano książkę to wyświetl co to za książka na sidebarze
if "selected_book" in st.session_state and st.session_state.selected_book:
    book = st.session_state.selected_book
    st.sidebar.info(f"Aktywna książka:\n## **{book.title}**\n\n**{book.author}**")
else:
    st.sidebar.info(f"Nie wybrano książki.")
st.sidebar.divider()

# Sidebar
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
elif page == "# Quiz":
    quiz_generator_view.show()
elif page == "# Admin":
    admin_view.show()

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