import streamlit as st

def show():
    st.title("Generator streszczeń")

    ai_service = st.session_state["ai_service"]

    # Załaduj książkę z kontekstu sesji
    selected_book = st.session_state.get("selected_book", None)
    if not selected_book:
        st.warning("Najpierw wybierz książkę we właściwym widoku.")
        return

    st.subheader(f"Wybrana książka: {selected_book.title}")
    st.markdown("Wygeneruj opracowanie książki za pomocą AI.")

    if selected_book.summary:
        st.markdown(f"### Streszczenie {selected_book.title}:")
        st.text_area("", selected_book.summary, height=400)

    if ai_service.is_summarizable(selected_book.content):
        if st.button("Wygeneruj streszczenie"):
            with st.spinner("Generuję streszczenie..."):
                selected_book.summary = ai_service.summarize_text(selected_book.content)
                st.success("Streszczenie wygenerowane!")

        if selected_book.summary:
            st.markdown(f"### Streszczenie {selected_book.title}:")
            st.text_area(selected_book.summary, height=400)
    else:
        st.error("Książka zbyt długa, aby streścić ją przy obecnej konfiguracji.")
