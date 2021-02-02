"""Record classes."""
import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from notebrowser.uri import URI, Library


@dataclass(frozen=True)
class Image:
    """A location file and metadata."""

    path: Path
    caption: str


StatBlock = dict[str, int]


@dataclass(frozen=True)
class Record:
    """A GM-note record."""

    name: str
    shortname: Optional[str] = None
    tagline: str = ""
    description: str = ""
    gallery: Optional[list[Image]] = None
    info: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Character(Record):
    """A base class for Character records."""

    cls: Optional[str] = None
    lvl: Optional[int] = None
    stats: Optional[StatBlock] = None


@dataclass(frozen=True)
class PlayerCharacter(Character):
    """Record for a Player Character."""

    player: Optional[str] = None


@dataclass(frozen=True)
class NonPlayerCharacter(Character):
    """Record for a Non-Player Character."""

    location: Optional[URI] = None
    faction: Optional[str] = None


@dataclass(frozen=True)
class Location(Record):
    """Record for a Location."""

    location: Optional[URI] = None


@dataclass(frozen=True)
class TextRecord(Record):
    """Base class for Records that are mainly free text."""

    date: Optional[datetime.date] = None
    text_body: str = ""
    text_references: set[URI] = field(default_factory=set)


@dataclass(frozen=True)
class Session(TextRecord):
    """Record for the log from a single session of play."""

    funfacts: Library[str] = field(default_factory=dict)


@dataclass(frozen=True)
class Note(TextRecord):
    """Record for miscellaneous notes."""

    topic: Optional[str] = None
