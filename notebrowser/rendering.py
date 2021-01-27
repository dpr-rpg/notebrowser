"""Functions for rendering pages."""
from pathlib import Path

from notebrowser.records import Record, RecordType
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


def create_record_toc(
    record_type: RecordType,
    library: Library[Record],
    toc_path: Path,
    record_page_dir: Path,
) -> None:
    """Create a table of contents page for records."""
    links = [
        record_link(uri, record, record_page_dir)
        for uri, record in library.items()
        if record.record_type == record_type
    ]
    content = (
        f"<h1>{record_type.value.capitalize()}s</h1>\n<ul>\n"
        + "".join(f"<li>{link}</li>\n" for link in links)
        + "</ul>"
    )
    with open(toc_path, "w") as f:
        f.write(content)
