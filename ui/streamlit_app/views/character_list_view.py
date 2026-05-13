import streamlit as st

def show():
    st.title("Bohaterzy utworu")

    # Ładujemy dane z pamięci sesji
    ai_service = st.session_state["ai_service"]
    selected_book = st.session_state.get("selected_book", None)

    # Logika wyświetlania
    if not selected_book:
        st.warning("Najpierw wybierz książkę.")
        return
    if selected_book.title:
        st.subheader(f"Wybrana książka: {selected_book.title}")
    if ai_service.is_summarizable(selected_book.content):
        if st.button("Wygeneruj opracowanie bohaterów"):
            with st.spinner("W trakcie..."):
                ai_ready_text = ai_service.clean_text(selected_book.content)
                selected_book.characters = ai_service.generate_characters_overview(ai_ready_text)
                st.rerun()
    else:
        st.error("Wybrany utwór nie może zostać opracowany.")
    if selected_book.characters:
        st.text_area(label="Opracowanie:", value=selected_book.characters, height=500, label_visibility="collapsed")
