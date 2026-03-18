class BookIndex:
    def __init__(
        self,
        full_sort_key: str,
        title: str,
        url: str,
        author: str,
        epoch: str,
        genre: str,
        kind: str,
        slug: str,
        href: str,
        downloaded: bool = False,
        path_to_file: str = None,
    ):
        self.full_sort_key = full_sort_key
        self.title = title
        self.url = url
        self.author = author
        self.epoch = epoch
        self.genre = genre
        self.kind = kind
        self.slug = slug
        self.href = href
        self.downloaded = downloaded
        self.path_to_file = path_to_file

    @staticmethod
    def from_raw_dict(data: dict) -> "BookIndex":
        return BookIndex(
            full_sort_key=data["full_sort_key"],
            title=data["title"],
            author=data["author"],
            kind=data["kind"],
            epoch=data["epoch"],
            genre=data["genre"],
            url=data["url"],
            href=data["href"],
            slug=data["slug"],
        )

    def to_dict(self) -> dict:
        return {
            "full_sort_key": self.full_sort_key,
            "title": self.title,
            "author": self.author,
            "kind": self.kind,
            "epoch": self.epoch,
            "genre": self.genre,
            "url": self.url,
            "href": self.href,
            "slug": self.slug,
            "downloaded": self.downloaded,
            "path_to_file": self.path_to_file,
        }

    def __repr__(self):
        return f"BookIndex(title={self.title}, author={self.author}, epoch={self.epoch}, genre={self.genre})"

    def __str__(self):
        return f"{self.title} – {self.author} ({self.epoch})"
