# Darkwing: Let's get IP-rangerous!
# Copyright (C) 2020 Mark E. Haase <mehaase@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
