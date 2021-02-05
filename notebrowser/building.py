"""Functions for building the site."""
import importlib.resources
import shutil
from dataclasses import astuple, dataclass, field
from pathlib import Path

from notebrowser import rendering
from notebrowser.assets import css, fonts
from notebrowser.loading import load_records
from notebrowser.sitedata import SiteData


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


def initialize_project_directory(base_dir: Path) -> None:
    """Create input data directory structure."""
    for d in Directories():
        (base_dir / d).mkdir(parents=True, exist_ok=True)


def deploy_default_assets(base_dir: Path) -> None:
    """Add default css and font files to assets."""
    dirs = Directories()
    _deploy_css(base_dir / dirs.css)
    _deploy_fonts(base_dir / dirs.fonts)


def make_site(base_dir: Path) -> SiteData:
    """Load data, clean site directory, and build site."""
    dirs = Directories()
    records = load_records(base_dir / dirs.records)
    site_data = SiteData(base_dir / dirs.site, records)
    pages = render_pages(site_data)
    clean(site_data)
    write_pages(site_data, pages)
    copy_assets(site_data, base_dir / dirs.assets)
    return site_data


def _deploy_fonts(font_dir: Path) -> None:
    if not font_dir.exists():
        font_dir.mkdir(parents=True)
    font_styles = ["regular", "bold", "italic", "bold_italic"]
    for style in font_styles:
        font_file = f"charter_{style}.woff2"
        font_data = importlib.resources.read_binary(fonts, font_file)
        with open(font_dir / font_file, "wb") as new_file:
            new_file.write(font_data)


def _deploy_css(css_dir: Path) -> None:
    stylesheet = "style.css"
    if not css_dir.exists():
        css_dir.mkdir(parents=True)
    css_data = importlib.resources.read_text(css, stylesheet)
    with open(css_dir / stylesheet, "w") as css_file:
        css_file.write(css_data)


def clean(site_data: SiteData) -> None:
    """Remove any existing site files."""
    if site_data.site_dir.exists():
        shutil.rmtree(site_data.site_dir)


def render_pages(site_data: SiteData) -> dict[Path, str]:
    """Create page content."""
    homepage = (site_data.homepage, rendering.render_homepage(site_data))
    record_pages = [
        (page, rendering.render_record_page(site_data, uri))
        for uri, page in site_data.record_pages.items()
    ]
    all_pages = [homepage] + record_pages
    return {
        path: rendering.apply_links(content, site_data) for path, content in all_pages
    }


def write_pages(site_data: SiteData, pages: dict[Path, str]) -> None:
    """Make directories and write pages to filesystem."""
    for page, content in pages.items():
        page_path = site_data.site_dir / page.relative_to(site_data.root)
        if not page_path.parent.exists():
            page_path.parent.mkdir(parents=True)
        with open(page_path, "w") as f:
            f.write(content)


def copy_assets(site_data: SiteData, asset_source: Path) -> None:
    """Copy assets to site directory."""
    asset_dest = site_data.site_dir / site_data.asset_dir.relative_to(site_data.root)
    if asset_source.exists():
        shutil.copytree(asset_source, asset_dest, dirs_exist_ok=True)
