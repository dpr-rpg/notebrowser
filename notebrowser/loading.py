"""Functions for loading campaign data."""

from pathlib import Path
from typing import Any, Callable, Dict, List, Type, TypeVar

import dacite
import frontmatter
import yaml

from notebrowser.campaigndata import CampaignData, Note, Session
from notebrowser.records import Record, RecordType
from notebrowser.uri import URI, Library, get_references


def load_campaign_data(data_dir: Path) -> CampaignData:
    """Read campaign data from `data_dir`."""
    return CampaignData(
        load_data(data_dir / "records", "*.yml", _parse_yaml_data, Record),
        load_data(data_dir / "sessions", "*.md", _parse_markdown_data, Session),
        load_data(data_dir / "notes", "*.md", _parse_markdown_data, Note),
    )


Data = TypeVar("Data", Record, Note, Session)
ConverterFunc = Callable[[List[str]], Dict[str, Any]]


def load_data(
    directory: Path,
    glob: str,
    to_dict: ConverterFunc,
    data_class: Type[Data],
) -> Library[Data]:
    """Load data."""
    contents = _read_files(directory, glob)
    data_dict = to_dict(contents)
    return {
        URI(k): from_dict(v, data_class, cast=[RecordType, URI])
        for k, v in data_dict.items()
    }


def from_dict(data: Dict[str, Any], data_class: Type[Data], cast: List[Type]) -> Data:
    """Convert Dict[str, Any] to Data object."""
    return dacite.from_dict(
        data=data,
        data_class=data_class,
        config=dacite.Config(cast=cast),
    )


def _parse_yaml_data(contents: List[str]) -> Dict[str, Any]:
    return yaml.safe_load("".join(contents))


def _parse_markdown_data(contents: List[str]) -> Dict[str, Any]:
    return {str(i): _parse_markdown_file_with_header(c) for i, c in enumerate(contents)}


def _parse_markdown_file_with_header(text: str) -> Dict[str, Any]:
    metadata, content = frontmatter.parse(text)
    references = get_references(content)
    return {"content": content, "references": references, **metadata}


def _read_files(base_dir: Path, glob: str) -> List[str]:
    files = [open(f, "r") for f in base_dir.rglob(glob)]
    contents = [f.read() for f in files]
    for f in files:
        f.close()
    return contents
