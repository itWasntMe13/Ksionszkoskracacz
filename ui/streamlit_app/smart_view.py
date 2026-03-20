import streamlit as st
from core.services.common.common_ai_service import GptService, CommonAiService
from core.config.gpt_config import GptConfig
from core.utils.ai_utils import count_gpt_tokens


def show():
    st.title("⚙️ Asystent AI")

    # Załaduj książkę z kontekstu sesji
    selected_book = st.session_state.get("selected_book", None)
    if not selected_book:
        st.warning("Najpierw wybierz książkę we właściwym widoku.")
        return

    # Konfiguracja AI
    ai_service = CommonAiService('Gemini')

    st.subheader(f"Książka: {selected_book.title}")
    st.markdown("Wygeneruj opracowanie książki za pomocą AI.")

    if ai_service.is_summarizable(selected_book.content):
        # Koszt streszczenia
        token_count = ai_service.count_tokens(selected_book.content)
        cost = token_count * 0.000002 / 1000 # Do poprawienia
        st.markdown(f"**Koszt streszczenia: {cost:.2f} PLN\tTokeny: {token_count}**\t Model: {ai_service.config.provider}")
        if st.button("📄 Wygeneruj streszczenie"):
            with st.spinner("Generuję streszczenie..."):
                summary = ai_service.summarize_text(selected_book.content)
                st.session_state["summary"] = summary
                st.success("Streszczenie wygenerowane!")

        if st.session_state.get("summary"):
            st.markdown(f"### 📘 Streszczenie {selected_book.title}:")
            st.text_area("Wynik:", st.session_state["summary"], height=400)
    else:
        st.error("📏 Książka zbyt długa, aby ją streścić przy obecnej konfiguracji.")
        token_count = ai_service.count_tokens(selected_book.content)
        st.markdown(
            f"**Tokeny w książce: {token_count}\tMaksymalna liczba tokenów do przetworzenia: {ai_service.config.max_tokens}**"
        ) # Do poprawienia
