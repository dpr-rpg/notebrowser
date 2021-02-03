"""Functions for loading campaign data."""

from collections import defaultdict
from pathlib import Path
from typing import Any

import dacite
import frontmatter
import yaml

from notebrowser.records import (
    Location,
    MarkdownText,
    NonPlayerCharacter,
    Note,
    PlayerCharacter,
    Record,
    Session,
)
from notebrowser.uri import URI, Library

_record_class_dict: defaultdict[str, type[Record]] = defaultdict(
    lambda: Record,
    session=Session,
    note=Note,
    pc=PlayerCharacter,
    npc=NonPlayerCharacter,
    location=Location,
)


def load_records(record_dir: Path) -> Library[Record]:
    """Load records found in .md and .yml files in record_dir."""
    yaml_files = _read_files(record_dir, "*.yml")
    markdown_files = _read_files(record_dir, "*.md")
    data_dict = _parse_yaml_data(yaml_files) | _parse_markdown_data(markdown_files)
    return {
        URI(k): record_from_dict(v, cast=[URI, Path, MarkdownText])
        for k, v in data_dict.items()
    }


def record_from_dict(data: dict[str, Any], cast: list[type]) -> Record:
    """Convert Dict[str, Any] to Record object."""
    return dacite.from_dict(
        data=data,
        data_class=_record_class_dict[data["record_type"]],
        config=dacite.Config(cast=cast),
    )


def _parse_yaml_data(contents: list[str]) -> dict[str, Any]:
    return yaml.safe_load("".join(contents))


def _parse_markdown_data(contents: list[str]) -> dict[str, Any]:
    data = [_parse_markdown_file_with_header(c) for c in contents]
    return {d["uri"]: d for d in data}


def _parse_markdown_file_with_header(text: str) -> dict[str, Any]:
    metadata, content = frontmatter.parse(text)
    return {"text_body": content, **metadata}


def _read_files(base_dir: Path, glob: str) -> list[str]:
    files = [open(f, "r") for f in base_dir.rglob(glob)]
    contents = [f.read() for f in files]
    for f in files:
        f.close()
    return contents
