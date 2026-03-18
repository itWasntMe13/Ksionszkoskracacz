# Funkcja dzieląca teksty wczytane z input_data na 3000 znakowe fragmenty
def split_text(text, fragment_length):
    # Lista fragmentów
    fragments = []
    # Długość tekstu
    text_length = len(text)
    # Ilość fragmentów
    fragments_amount = text_length // fragment_length
    # Dzielenie tekstu na fragmenty
    for i in range(fragments_amount):
        fragments.append(text[i * fragment_length : (i + 1) * fragment_length])
    # Dodanie reszty tekstu, jeśli została
    if text_length % fragment_length != 0:
        fragments.append(text[fragments_amount * fragment_length :])
    return fragments
