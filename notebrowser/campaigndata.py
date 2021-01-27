"""Classes for storing campaign data."""
from dataclasses import dataclass, field
from datetime import date
from typing import Set

from notebrowser.records import Record
from notebrowser.uri import URI, Library


@dataclass(frozen=True)
class Session:
    """Notes from a single session of play."""

    date: date
    summary: str
    content: str
    references: Set[URI]
    funfacts: Library[str] = field(default_factory=dict)


@dataclass(frozen=True)
class Note:
    """Miscellaneous notes."""

    title: str
    date: date
    content: str
    references: Set[URI]


@dataclass(frozen=True)
class CampaignData:
    """Container for all of the input data for the campaign."""

    records: Library[Record]
    sessions: Library[Session]
    notes: Library[Note]
