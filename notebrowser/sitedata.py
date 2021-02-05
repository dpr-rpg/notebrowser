"""Class for storing the directory structure of the site."""
from dataclasses import dataclass, field
from pathlib import Path

from notebrowser.configuration import Configuration
from notebrowser.records import Record
from notebrowser.uri import Library


@dataclass(frozen=True)
class SiteData:
    """Container for site data."""

    _root = Path("/")
    _assets = _root / "assets"
    root: Path = field(init=False, default=_root)
    record_page_dir: Path = field(init=False, default=_root / "records")
    asset_dir: Path = field(init=False, default=_assets)
    css_dir: Path = field(init=False, default=_assets / "css")
    font_dir: Path = field(init=False, default=_assets / "font")
    img_dir: Path = field(init=False, default=_assets / "img")
    homepage: Path = field(init=False, default=_root / "home.html")

    site_dir: Path
    records: Library[Record]
    config: Configuration

    record_pages: Library[Path] = field(init=False)

    def __post_init__(self):
        """Compute record page urls."""
        object.__setattr__(
            self,
            "record_pages",
            {uri: self.record_page_dir / f"{uri.uri}.html" for uri in self.records},
        )
