"""Classes for storing campaign data."""
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Set

import dacite
import frontmatter
import yaml

from notebrowser.records import URI, RecordLibrary, RecordType, get_references


@dataclass(frozen=True)
class Session:
    """Notes from a single session of play."""

    date: date
    summary: str
    content: str
    references: Set[URI]
    funfacts: Dict[URI, str] = field(default_factory=dict)


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

    records: RecordLibrary
    sessions: List[Session]
    notes: List[Note]


def load_campaign_data(data_dir: Path) -> CampaignData:
    """Read campaign data from `data_dir`."""
    records = load_records(data_dir / "records")
    sessions = load_sessions(data_dir / "sessions")
    notes: List[Note] = load_notes(data_dir / "notes")
    return CampaignData(records, sessions, notes)


def _read_files(base_dir: Path, glob: str) -> List[str]:
    files = [open(f, "r") for f in base_dir.rglob(glob)]
    contents = [f.read() for f in files]
    for f in files:
        f.close()
    return contents


def load_records(record_dir: Path) -> RecordLibrary:
    """Load records from `record_dir`."""
    contents = _read_files(record_dir, "*.yml")
    record_dict = yaml.safe_load("".join(contents))
    return records_from_dict(record_dict)


def load_sessions(session_dir: Path) -> List[Session]:
    """Load sessions from `session_dir`."""
    contents = _read_files(session_dir, "*.md")
    return [_parse_session(c) for c in contents]


def load_notes(note_dir: Path) -> List[Note]:
    """Load notes from `note_dir`."""
    contents = _read_files(note_dir, "*.md")
    return [_parse_note(c) for c in contents]


def _read_markdown_with_header(text: str) -> Dict[str, Any]:
    metadata, content = frontmatter.parse(text)
    references = get_references(content)
    return {"content": content, "references": references, **metadata}


def _parse_note(note_text: str) -> Note:
    data = _read_markdown_with_header(note_text)
    return dacite.from_dict(
        data_class=Note, data=data, config=dacite.Config(cast=[URI])
    )


def _parse_session(session_text: str) -> Session:
    data = _read_markdown_with_header(session_text)
    return dacite.from_dict(
        data_class=Session, data=data, config=dacite.Config(cast=[URI])
    )


def records_from_dict(record_dict: Dict[str, Any]) -> RecordLibrary:
    """Import records from a dictionary from a yaml file."""
    return dacite.from_dict(
        data_class=RecordLibrary,
        data={"records": record_dict},
        config=dacite.Config(cast=[RecordType, URI]),
    )
