import streamlit as st

def show():
    st.title("Bohaterzy utworu")

    # Ładujemy dane z pamięci sesji
    ai_service = st.session_state["ai_service"]
    selected_book = st.session_state.get("selected_book", None)

    if not selected_book:
        st.warning("Najpierw wybierz książkę.")
        return

    st.subheader(f"Wybrana książka: {selected_book.title}")

    if selected_book.characters:
        st.text_area("Opracowanie:", selected_book.characters, height=600)
    if ai_service.is_summarizable(selected_book.content):
        if st.button("Wygeneruj opracowanie bohaterów"):
            with st.spinner("W trakcie..."):
                selected_book.characters = ai_service.generate_characters_overview(selected_book.content)
                st.rerun()
    else:
        st.error("Wybrany utwór nie może zostać opracowany.")