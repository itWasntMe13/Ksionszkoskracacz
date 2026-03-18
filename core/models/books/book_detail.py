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
        return BookDetail(
            title=data.get("title"),
            txt_url=data.get("txt"),
            author=data.get("authors", [{}])[0].get("name"),
            epoch=data.get("epochs", [{}])[0].get("name"),
            genre=data.get("genres", [{}])[0].get("name"),
        )

    @staticmethod
    def from_json_dict(data: dict) -> "BookDetail":
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
        return {
            "slug": self.slug,
            "title": self.title,
            "txt_url": self.txt_url,
            "author": self.author,
            "kind": self.kind,
            "epoch": self.epoch,
            "genre": self.genre,
        }
