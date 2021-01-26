"""Record classes and derived info structures."""
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, ItemsView, List, Optional, Set

re_slug = re.compile(r"^[-a-zA-Z0-9_]+$")
re_ref = re.compile(r"\{([-a-zA-Z0-9_]+)\}")


def get_references(content: str) -> Set[str]:
    """Get the unique set of references in a string."""
    return set(re_ref.findall(content))


def _is_slug(value: str) -> bool:
    match = re_slug.match(value)
    if match:
        return True
    else:
        return False


@dataclass(frozen=True)
class URI:
    """A unique record identifier. Safe for use in URLs and filenames."""

    uri: str

    def __post_init__(self) -> None:
        """Validate URI."""
        if not _is_slug(self.uri):
            raise ValueError(
                f'Invalid URI: "{self.uri})".'
                + "May only contain alphanumeric characters, hyphens, and underscores."
            )

    def __str__(self) -> str:
        """Return the URI as a string."""
        return self.uri


class RecordType(Enum):
    """Enumerated record types."""

    PC = "pc"
    NPC = "npc"
    LOCATION = "location"


@dataclass(frozen=True)
class Image:
    """A location file and metadata."""

    path: Path
    caption: str


StatBlock = Dict[str, int]


@dataclass(frozen=True)
class Record:
    """A GM-note record."""

    record_type: RecordType
    name: str
    shortname: str
    tagline: str = ""
    description: str = ""
    location: Optional[URI] = None
    cls: Optional[str] = None
    lvl: Optional[int] = None
    stats: Optional[StatBlock] = None
    gallery: Optional[List[Image]] = None
    info: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RecordTree:
    """A tree data structure with records as nodes."""

    record: Optional[Record] = None
    children: List["RecordTree"] = field(default_factory=list)


@dataclass(frozen=True)
class RecordLibrary:
    """A collection of Records indexed by URI strings."""

    records: Dict[URI, Record]

    def __getitem__(self, uri: URI) -> Record:
        """Get records by uri."""
        return self.records[uri]

    def items(self) -> ItemsView[URI, Record]:
        """Get (uri, record) pairs."""
        return self.records.items()
