"""Classes for storing campaign data."""
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Set, Type, TypeVar

import dacite
import frontmatter
import yaml

from notebrowser.records import RecordLibrary, RecordType
from notebrowser.uri import URI, get_references


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


FromMd = TypeVar("FromMd", Note, Session)


@dataclass(frozen=True)
class CampaignData:
    """Container for all of the input data for the campaign."""

    records: RecordLibrary
    sessions: List[Session]
    notes: List[Note]


def load_campaign_data(data_dir: Path) -> CampaignData:
    """Read campaign data from `data_dir`."""
    records: RecordLibrary = load_records(data_dir / "records")
    sessions: List[Session] = load_from_markdown(data_dir / "sessions", Session)
    notes: List[Note] = load_from_markdown(data_dir / "notes", Note)
    return CampaignData(records, sessions, notes)


def load_records(record_dir: Path) -> RecordLibrary:
    """Load records from YAML files in `record_dir`."""
    contents = _read_files(record_dir, "*.yml")
    record_dict = yaml.safe_load("".join(contents))
    return _records_from_dict(record_dict)


def load_from_markdown(directory: Path, data_class: Type[FromMd]) -> List[FromMd]:
    """Load Sessions or Notes from markdown files with headers."""
    contents = _read_files(directory, "*.md")
    return [_parse_markdown_with_header(c, data_class) for c in contents]


def _read_files(base_dir: Path, glob: str) -> List[str]:
    files = [open(f, "r") for f in base_dir.rglob(glob)]
    contents = [f.read() for f in files]
    for f in files:
        f.close()
    return contents


def _parse_markdown_with_header(text: str, data_class: Type[FromMd]) -> FromMd:
    metadata, content = frontmatter.parse(text)
    references = get_references(content)
    data = {"content": content, "references": references, **metadata}
    return dacite.from_dict(
        data_class=data_class, data=data, config=dacite.Config(cast=[URI])
    )


def _records_from_dict(record_dict: Dict[str, Any]) -> RecordLibrary:
    """Import records from a dictionary from a yaml file."""
    return dacite.from_dict(
        data_class=RecordLibrary,
        data={"records": record_dict},
        config=dacite.Config(cast=[RecordType, URI]),
    )
