import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from ui.streamlit_app import main_view, admin_view, smart_view

# taskkill /f /im streamlit.exe - zabij wszystkie procesy streamlit.exe
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
