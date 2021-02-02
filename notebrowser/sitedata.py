"""Class for storing the directory structure of the site."""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SiteData:
    """Container for site data."""

    site_dir: Path
    record_page_dir: Path
    session_page_dir: Path
    note_page_dir: Path

    home_page: Path
    session_toc_page: Path
    note_toc_page: Path


def create_site_data(base_dir: Path) -> SiteData:
    """Create site SiteData."""
    site_dir = base_dir / "site"
    return SiteData(
        site_dir,
        site_dir / "records",
        site_dir / "sessions",
        site_dir / "notes",
        site_dir / "home.html",
        site_dir / "session_toc.html",
        site_dir / "note_toc.html",
    )
