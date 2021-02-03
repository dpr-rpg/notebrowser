"""Record classes."""
import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from mistune import markdown

from notebrowser.uri import URI, Library, get_references


@dataclass(frozen=True)
class MarkdownText:
    """A block of markdown text."""

    text: str

    def __str__(self):
        """Render markdown text as html."""
        return markdown(self.text)


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
    description: MarkdownText = MarkdownText("")
    gallery: Optional[list[Image]] = None
    info: dict[str, str] = field(default_factory=dict)
    references: set[URI] = field(init=False)

    def __post_init__(self):
        """Extract references from description."""
        references = get_references(self.description.text)
        object.__setattr__(self, "references", references)


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
    text_body: MarkdownText = MarkdownText("")

    def __post_init__(self):
        """Extract references from description and body text."""
        references = get_references(self.description.text) | get_references(
            self.text_body.text
        )
        object.__setattr__(self, "references", references)


@dataclass(frozen=True)
class Session(TextRecord):
    """Record for the log from a single session of play."""

    funfacts: Library[str] = field(default_factory=dict)


@dataclass(frozen=True)
class Note(TextRecord):
    """Record for miscellaneous notes."""

    topic: Optional[str] = None
