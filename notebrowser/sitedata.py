"""Class for storing the directory structure of the site."""
import importlib.resources
from dataclasses import dataclass
from pathlib import Path

import notebrowser.templates
from notebrowser.loading import load_records
from notebrowser.records import Record
from notebrowser.uri import URI, Library


@dataclass(frozen=True)
class SiteData:
    """Container for site data."""

    site_dir: Path
    asset_dir: Path
    homepage: Path

    records: Library[Record]
    record_page_dir: Path
    record_pages: Library[Path]

    stylesheet_path: Path
    stylesheet_content: str


def record_page_url(record_page_dir: Path, uri: URI) -> Path:
    """Return the URL for a record page."""
    return record_page_dir / f"{uri.uri}.html"


def create_site_data(base_dir: Path) -> SiteData:
    """Create site SiteData."""
    site_dir = base_dir / "site"
    asset_dir = site_dir / "assets"
    record_source_dir = base_dir / "records"
    records = load_records(record_source_dir)
    record_page_dir = site_dir / "records"
    record_pages = {uri: record_page_url(record_page_dir, uri) for uri in records}
    return SiteData(
        site_dir,
        asset_dir,
        site_dir / "home.html",
        records,
        record_page_dir,
        record_pages,
        asset_dir / "style.css",
        importlib.resources.read_text(notebrowser.templates, "style.css"),
    )
