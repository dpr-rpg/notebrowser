"""Class for storing the directory structure of the site."""
from dataclasses import dataclass
from pathlib import Path

from notebrowser.loading import load_records
from notebrowser.records import Record
from notebrowser.uri import URI, Library


@dataclass(frozen=True)
class SiteData:
    """Container for site data."""

    site_dir: Path
    homepage: Path

    records: Library[Record]
    record_page_dir: Path
    record_pages: Library[Path]


def record_page_url(record_page_dir: Path, uri: URI) -> Path:
    """Return the URL for a record page."""
    return record_page_dir / f"{uri.uri}.html"


def create_site_data(base_dir: Path) -> SiteData:
    """Create site SiteData."""
    site_dir = base_dir / "site"
    record_source_dir = base_dir / "records"
    records = load_records(record_source_dir)
    record_page_dir = site_dir / "records"
    record_pages = {uri: record_page_url(record_page_dir, uri) for uri in records}
    return SiteData(
        site_dir, site_dir / "home.html", records, record_page_dir, record_pages
    )
