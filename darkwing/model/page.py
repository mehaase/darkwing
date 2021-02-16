from dataclasses import dataclass
import typing


T = typing.TypeVar("T")


@dataclass
class PageRequest:
    """
    Represents a request for a page from a result set.
    """

    page_number: int
    items_per_page: int
    sort_column: str
    sort_ascending: bool

    @staticmethod
    def from_json(json: dict):
        return PageRequest(
            json["page_number"],
            json["items_per_page"],
            json["sort_column"],
            json["sort_ascending"],
        )


@dataclass
class PageResult:
    """
    Represents a page containing a result set.
    """

    total_count: int
    items: typing.List[typing.Any]

    def serialize(self, serialize_fn) -> dict:
        return {
            "total_count": self.total_count,
            "items": [serialize_fn(i) for i in self.items],
        }
