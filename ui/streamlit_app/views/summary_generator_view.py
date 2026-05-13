import streamlit as st

st.title("Generator streszczeń")

# Ładujemy dane z pamięci sesji
ai_service = st.session_state["ai_service"]
selected_book = st.session_state.get("selected_book")

# Logika wyświetlania
if not selected_book:
    st.warning("Najpierw wybierz książkę.")
else:
    if selected_book.title:
        st.subheader(f"Wybrana książka: {selected_book.title}")
    if ai_service.is_summarizable(selected_book.content):
        if st.button("Wygeneruj streszczenie"):
            with st.spinner("W trakcie..."):
                ai_ready_text = ai_service.clean_text(selected_book.content)
                selected_book.summary = ai_service.summarize_text(ai_ready_text)
                st.rerun()
    else:
        st.error("Wybrany utwór nie może zostać opracowany.")
    if selected_book.summary:
        st.text_area(label="Opracowanie:", value=selected_book.summary, height=500, label_visibility="collapsed")