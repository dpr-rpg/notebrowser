"""Configuration class."""

from dataclasses import asdict, astuple, dataclass, field
from pathlib import Path

import dacite
import yaml

from notebrowser import records
from notebrowser.records import Record
from notebrowser.uri import Library

CONFIGFILE = Path("notebrowser.yml")


@dataclass(frozen=True)
class Configuration:
    """Project configuration."""

    title: str = "Title"
    author: str = "Author"
    stylesheet: str = "style.css"
    record_tocs: list[str] = field(
        default_factory=lambda: [
            "Session",
            "Note",
            "PlayerCharacter",
            "NonPlayerCharacter",
            "Location",
        ]
    )

    def to_file(self, config_file: Path):
        """Write configuration to file."""
        with open(config_file, "w") as f:
            yaml.dump(asdict(self), f)


def load_configuration(config_file: Path) -> Configuration:
    """Read configuration file."""
    with open(config_file) as f:
        data = yaml.safe_load(f)
    return dacite.from_dict(data=data, data_class=Configuration)


@dataclass(frozen=True)
class Directories:
    """The project's directory structure."""

    records: Path = field(init=False, default=Path("records"))
    site: Path = field(init=False, default=Path("site"))
    _assets = Path("assets")
    assets: Path = field(init=False, default=_assets)
    css: Path = field(init=False, default=_assets / "css")
    fonts: Path = field(init=False, default=_assets / "fonts")
    img: Path = field(init=False, default=_assets / "img")

    def __iter__(self):
        """Iterate over directories."""
        return iter(astuple(self))


@dataclass(frozen=True)
class SiteData:
    """Container for site data."""

    _root = Path("/")
    _assets = _root / "assets"
    root: Path = field(init=False, default=_root)
    record_page_dir: Path = field(init=False, default=_root / "records")
    asset_dir: Path = field(init=False, default=_assets)
    css_dir: Path = field(init=False, default=_assets / "css")
    font_dir: Path = field(init=False, default=_assets / "fonts")
    img_dir: Path = field(init=False, default=_assets / "img")
    homepage: Path = field(init=False, default=_root / "home.html")

    site_dir: Path
    records: Library[Record]
    config: Configuration

    record_pages: Library[Path] = field(init=False)
    toc_pages: dict[type[Record], Path] = field(init=False)

    def __post_init__(self):
        """Compute record and toc page urls."""
        object.__setattr__(
            self,
            "record_pages",
            {uri: self.record_page_dir / f"{uri.uri}.html" for uri in self.records},
        )
        object.__setattr__(
            self,
            "toc_pages",
            {
                records.__getattribute__(rt): self.root / f"{rt}-toc.html"
                for rt in self.config.record_tocs
            },
        )
