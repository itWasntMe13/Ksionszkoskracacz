import streamlit as st

def show():
    st.title("Bohaterzy utworu")

    ai_service = st.session_state["ai_service"]

    # Załaduj książkę z kontekstu sesji
    selected_book = st.session_state.get("selected_book", None)
    if not selected_book:
        st.warning("Najpierw wybierz książkę we właściwym widoku.")
        return

    st.subheader(f"Wybrana książka: {selected_book.title}")
    st.markdown("Wygeneruj opracowanie książki za pomocą AI.")