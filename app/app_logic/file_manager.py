import glob
import datetime
import os


# Funkcja wczytująca plik o podanej ścieżce
def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"An error occurred while loading a file: {e}"


# Funkcja dodająca treść do pliku o podanej ścieżce
def append_file(path, content):
    # Jeśli plik nie istnieje, zostanie utworzony
    if not glob.glob(path):
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(f"{datetime.datetime.now}\n")  # Dodajemy datę i godzinę
                file.write(content)  # Dodajemy treść
                file.write("\n" + "-" * 50 + "\n\n")  # Dodajemy znacznik końca wpisu
        except Exception as e:
            return f"An error occurred while creating a new file: {e}"
    else:
        try:
            with open(path, "a", encoding="utf-8") as file:
                file.write(f"{datetime.datetime.now()}\n")  # Dodajemy datę i godzinę
                file.write(content)  # Dodajemy treść
                file.write("\n" + "-" * 50 + "\n\n")  # Dodajemy znacznik końca wpisu
        except Exception as e:
            return f"An error occurred while appending to an existing file: {e}"


# Funkcja zapisująca treść do pliku o podanej ścieżce
def save_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(f"{datetime.datetime.now()}\n")  # Dodajemy datę i godzinę
            file.write(content)  # Dodajemy treść
    except Exception as e:
        return f"An error occurred: {e}"


# Funkcja tworząca folder o podanej ścieżce
def create_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        return f"An error occurred while creating a folder: {e}"


# Funkcja łącząca kawałki streszczeń w jeden string
def merge_txt_files(path) -> str:
    # Pobieramy listę plików z podanego katalogu
    files = glob.glob(f"{path}/*.txt")

    # Tworzymy pusty string, do którego będziemy dodawać treść plików
    merged_text = ""

    # Dla każdego pliku w katalogu
    for file in files:
        # Wczytujemy treść pliku
        text = load_file(file)
        # Dodajemy treść pliku do stringa
        merged_text += text

    # Zwracamy połączony tekst
    return merged_text
