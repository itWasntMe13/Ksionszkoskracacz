import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from ui.streamlit_app import helpers
from ui.config.providers import AiProviders

# Ustawiamy logo i favicon
st.set_page_config(page_title="Ksionszkoskracacz", page_icon='ui/img/favicon.ico', layout="wide")
# Zwiększamy logo manualnie
st.html("""
  <style>
    [alt=Logo] {
        height: 150px;
        width: auto;
        margin: auto;
    }
  </style>
        """)
st.logo('ui/img/main_logo.png')

# Definiujemy podstrony
views_path = "./views"
print(f"{views_path}/choose_a_book_view.py")
books_view = st.Page(f"{views_path}/choose_a_book_view.py", title="Wybór książki")
summary_view = st.Page(f"{views_path}/summary_generator_view.py", title="Generator streszczeń")
character_view = st.Page(f"{views_path}/character_list_view.py", title="Lista bohaterów")
motifs_view = st.Page(f"{views_path}/motifs_view.py", title="Lista motywów")
quiz_view = st.Page(f"{views_path}/quiz_generator_view.py", title="Quiz")
admin_panel_view = st.Page(f"{views_path}/admin_view.py", title="Admin")

pg = st.navigation([books_view, summary_view, character_view, motifs_view ,quiz_view, admin_panel_view], position="sidebar")
pg.run()

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
# Wywołanie inicjalizatora AiService z domyslnym providerem
helpers.init_ai_service(AiProviders.GEMINI.value)


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