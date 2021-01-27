"""Record classes and derived info structures."""
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from notebrowser.uri import URI


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
