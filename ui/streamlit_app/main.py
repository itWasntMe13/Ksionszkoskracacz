import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from ui.streamlit_app import main_view, admin_view, smart_view
from core.services.common.common_ai_service import CommonAiService

# taskkill /f /im streamlit.exe - zabij wszystkie procesy streamlit.exe

if "ai_service" not in st.session_state:
    try:
        api_key = st.secrets["api_key"]


# Sidebar – nawigacja
st.sidebar.title("📚 Nawigacja")
page = st.sidebar.radio(
    "Wybierz tryb:", ["📖 Wybór książki", "⚙️ Asystent AI", "🛠️ Admin"]
)

# Widoki
if page == "📖 Wybór książki":
    main_view.show()
elif page == "⚙️ Asystent AI":
    smart_view.show()
elif page == "🛠️ Admin":
    admin_view.show()
