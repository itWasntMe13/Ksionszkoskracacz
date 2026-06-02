import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "..")))
import streamlit as st
from core.services.common.maintenance_service import MaintenanceService

# Inicjalizacja zmiennej potwierdzającej usunięcie książek żeby potwierdzenie działało
if "delete_requested" not in st.session_state:
    st.session_state.delete_requested = False

st.title("Panel administracyjny")
st.markdown(
    "Opcje zarządzania aplikacją. Niektóre funkcjonalności pozwalają na serwisowe rozwiązywanie problemów aplikacji."
)

# Budowa katalogów. To jest ważne!
if st.button("Utwórz katalogi na dane wejściowe"):
    MaintenanceService.build_environment()
    st.success("Katalogi zostały utworzone.")

# Pierwszy button zapisuje nam info że użytkownik chce usunąć książki.
if st.button("Usuń wszystkie książki oraz ich szczegóły"):
    st.session_state.delete_requested = True

# Strona się odświeża, wczytujemy zmienną z sesji, jeśli jest true to znaczy że użytkownik próbuje usunąć książki.
if st.session_state.delete_requested:
    st.warning("Aby potwierdzić usunięcie, kliknij ponownie przycisk.")

    if st.button("Potwierdź usunięcie", key="confirm_delete_books"):
        MaintenanceService.clear_books_dir()
        MaintenanceService.clear_books_details_dir()

        st.success("Książki oraz ich szczegóły zostały usunięte.")

        st.session_state.delete_requested = False


if st.button("Zaktualizuj indeks książek"):
    MaintenanceService.create_book_indexes(force_update=True)
    st.success("Indeks został zaktualizowany.")
