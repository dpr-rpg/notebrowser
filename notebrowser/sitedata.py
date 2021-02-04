"""Class for storing the directory structure of the site."""
from dataclasses import dataclass
from pathlib import Path

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

    stylesheet_dir: Path
    stylesheet: Path

    font_dir: Path

    img_dir: Path


def record_page_url(record_page_dir: Path, uri: URI) -> Path:
    """Return the URL for a record page."""
    return record_page_dir / f"{uri.uri}.html"


def create_site_data(site_dir: Path, records: Library[Record]) -> SiteData:
    """Create site SiteData."""
    root = Path("/")
    asset_dir = root / "assets"
    record_page_dir = root / "records"
    record_pages = {uri: record_page_url(record_page_dir, uri) for uri in records}
    return SiteData(
        site_dir=site_dir,
        asset_dir=asset_dir,
        homepage=root / "home.html",
        records=records,
        record_page_dir=record_page_dir,
        record_pages=record_pages,
        stylesheet_dir=asset_dir / "css",
        img_dir=asset_dir / "img",
        stylesheet=Path("style.css"),
        font_dir=asset_dir / "fonts",
    )
