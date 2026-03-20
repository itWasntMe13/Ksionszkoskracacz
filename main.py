# WAŻNE - PROGRAM KORZYSTA Z BIBLIOTEKI OPENAI==0.28
from core.services.common.common_ai_service import BaseAiService

if __name__ == "__main__":

    # """
    # Budowa środowiska.
    # """
    # setup.build_environment() # Budujemy środowisko
    #
    # """
    # Obsługa API Wolnych Lektur od pobrania surowego indeksu książek do pobrania książki.
    # """
    # book_index_raw_service.BookIndexRawService.download_books_index_raw_json() # Pobranie surowego indeksu książek
    # book_index_service.BookIndexService.create_books_index_json() # Stworzenie pliku JSON z "naszym" indeksem książek
    # book_index_list = book_index_service.BookIndexService.load_books_index_json() # Wczytanie indeksu książek
    # chosen_book_index = book_browsing_service.BookBrowsingService.choose_a_book(book_index_list) # Wybór książki zwraca obiekt BookIndex
    # book_detail_service.BookDetailService.download_book_details_json(chosen_book_index) # Pobranie detali książki na podstawie obiektu BookIndex
    # book_detail = book_detail_service.BookDetailService.load_book_details_json(chosen_book_index) # Wczytanie detali książki w formie obiektu BookDetail
    # book = book_service.BookService.create_book_object(book_detail, save=True) # Pobranie treści książki i zapisanie jej do pliku JSON
    #
    # """
    # Na ten moment mamy wszystkie dane i pliki książek/książki.
    # Od teraz zamykamy komunikację z API Wolnych Lektur i przechodzimy do komunikacji z OpenAI.
    # """
    #
    # GPT

    ai_service = BaseAiService()
