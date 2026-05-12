import streamlit as st

def show():
    st.title("Generator streszczeń")

    # Ładujemy dane z pamięci sesji
    ai_service = st.session_state["ai_service"]
    selected_book = st.session_state.get("selected_book")

    if not selected_book:
        st.warning("Najpierw wybierz książkę.")
        return

    st.subheader(f"Wybrana książka: {selected_book.title}")

    if selected_book.summary:
        st.text_area("Streszczenie", selected_book.summary, height=600)
    if ai_service.is_summarizable(selected_book.content):
        if st.button("Wygeneruj streszczenie"):
            with st.spinner("W trakcie..."):
                selected_book.summary = ai_service.summarize_text(selected_book.content)
                st.rerun()
    else:
        st.error("Wybrany utwór nie może zostać opracowany.")
