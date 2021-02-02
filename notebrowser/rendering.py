"""Functions for rendering pages."""
from pathlib import Path

from notebrowser.records import Record
from notebrowser.uri import URI, Library


def html_link(path: Path, text: str) -> str:
    """Generate an html link."""
    return f'<a href="{path}">{text}</a>'


def record_path(uri: URI, record_page_dir: Path) -> Path:
    """Generate path to a record page."""
    return record_page_dir / f"{uri}.html"


def record_link(uri: URI, record: Record, record_page_dir: Path) -> str:
    """Generate a link to a record page."""
    path = record_path(uri, record_page_dir)
    name = record.name
    return html_link(path, name)


def create_record_pages(library: Library[Record], record_page_dir: Path) -> None:
    """Create pages for all records in a library."""
    assert record_page_dir.exists()
    assert record_page_dir.is_dir()
    for uri, record in library.items():
        path = record_path(uri, record_page_dir)
        content = str(library[uri])
        with open(path, "w") as f:
            f.write(content)
