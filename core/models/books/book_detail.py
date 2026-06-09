from dataclasses import dataclass
from typing import Optional


@dataclass
class BookDetail:
    title: str
    txt_url: str
    author: str
    epoch: str
    genre: str
    kind: Optional[str] = None
    slug: Optional[str] = None

    @staticmethod
    def from_api_dict(data: dict) -> "BookDetail":
        """
        Konstruktor fabryczny. Tworzy instancję klasy BookDetail na podstawie surowych danych z API Wolnych Lektur.
        :param data:
        :return:
        """
        return BookDetail(
            title=data.get("title"),
            txt_url=data.get("txt"),
            author=data.get("authors", [{}])[0].get("name"),
            epoch=data.get("epochs", [{}])[0].get("name"),
            genre=data.get("genres", [{}])[0].get("name"),
        )

    @staticmethod
    def from_dict(data: dict) -> "BookDetail":
        """
            Konstruktor fabryczny. Tworzy instancję klasy BookDetail na podstawie słownika danych przekazanego w parametrze.
            Metoda służy m.in. do utworzenia obiektu na podstawie słownika uzyskanego po deserializacji pliku JSON.
            :param data: dict
            :return: BookDetail
        """
        return BookDetail(
            slug=data.get("slug"),
            title=data.get("title"),
            txt_url=data.get("txt_url"),
            author=data.get("author"),
            kind=data.get("kind"),
            epoch=data.get("epoch"),
            genre=data.get("genre"),
        )

    def to_dict(self) -> dict:
        """
            Dokonuje eksportu stanu obiektu do słownika. Metoda służy, np. do przygotowania danych w formacie słownika do dalszej serializacji do formatu JSON.
            :return: dict
            """
        return {
            "slug": self.slug,
            "title": self.title,
            "txt_url": self.txt_url,
            "author": self.author,
            "kind": self.kind,
            "epoch": self.epoch,
            "genre": self.genre,
        }
