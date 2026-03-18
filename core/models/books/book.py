from dataclasses import dataclass


@dataclass
class Book:
    slug: str
    title: str
    author: str
    kind: str
    epoch: str
    genre: str
    content: str
    short_description: str = None
    summary: str = None
    characters: str = None
    test_questions: str = None
    motifs: str = None

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "title": self.title,
            "author": self.author,
            "kind": self.kind,
            "epoch": self.epoch,
            "genre": self.genre,
            "content": self.content,
            "short_description": self.short_description,
            "summary": self.summary,
            "characters": self.characters,
            "test_questions": self.test_questions,
            "motifs": self.motifs,
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        return Book(
            slug=data.get("slug"),
            title=data.get("title"),
            author=data.get("author"),
            kind=data.get("kind"),
            epoch=data.get("epoch"),
            genre=data.get("genre"),
            content=data.get("content"),
            short_description=data.get("short_description"),
            summary=data.get("summary"),
            characters=data.get("characters"),
            test_questions=data.get("test_questions"),
            motifs=data.get("motifs"),
        )
