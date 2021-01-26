"""Functions for rendering pages."""
from pathlib import Path

from notebrowser.records import URI, Record, RecordLibrary


def html_link(path: Path, text: str) -> str:
    """Generate an html link."""
    return f'<a href="{path}">{text}</a>'


def record_path(uri: URI, record_dir: Path) -> Path:
    """Generate path to a record page."""
    return record_dir / f"{uri}.html"


def record_link(uri: URI, record: Record, record_dir: Path) -> str:
    """Generate a link to a record page."""
    path = record_path(uri, record_dir)
    name = record.name
    return html_link(path, name)


def create_record_pages(library: RecordLibrary, record_dir: Path) -> None:
    """Create pages for all records in a library."""
    assert record_dir.exists()
    assert record_dir.is_dir()
    for uri, record in library.items():
        path = record_path(uri, record_dir)
        content = str(library[uri])
        with open(path, "w") as f:
            f.write(content)


def create_record_toc(library: RecordLibrary, toc_path: Path, record_dir: Path) -> None:
    """Create a table of contents page for records."""
    links = [record_link(uri, record, record_dir) for uri, record in library.items()]
    content = (
        "<h1>Records</h1>\n<ul>\n"
        + "".join(f"<li>{link}</li>\n" for link in links)
        + "</ul>"
    )
    with open(toc_path, "w") as f:
        f.write(content)
