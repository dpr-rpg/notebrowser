"""Functions for building the site."""
import importlib.resources
import shutil
from pathlib import Path

from notebrowser import rendering
from notebrowser.assets import css, fonts
from notebrowser.loading import load_records
from notebrowser.sitedata import SiteData, create_site_data


def make_site(base_dir: Path) -> SiteData:
    """Load data, clean site directory, and build site."""
    records = load_records(base_dir / "records")
    site_data = create_site_data(base_dir / "site", records)
    pages = render_pages(site_data)
    clean(site_data)
    write_pages(site_data, pages)
    deploy_assets(site_data, base_dir / "assets")
    return site_data


def deploy_assets(site_data: SiteData, asset_source: Path) -> None:
    """Add css and font files to site assets."""
    font_dir = site_data.site_dir / site_data.font_dir.relative_to("/")
    css_dir = site_data.site_dir / site_data.stylesheet_dir.relative_to("/")
    asset_dest = site_data.site_dir / site_data.asset_dir.relative_to("/")
    _deploy_fonts(font_dir)
    _deploy_css(css_dir)
    _copy_assets(asset_dest, asset_source)


def _copy_assets(asset_dest: Path, asset_source: Path) -> None:
    if asset_source.exists():
        shutil.copytree(asset_source, asset_dest, dirs_exist_ok=True)


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
    with open(css_dir / "style.css", "w") as css_file:
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
        page_path = site_data.site_dir / page.relative_to("/")
        if not page_path.parent.exists():
            page_path.parent.mkdir(parents=True)
        with open(page_path, "w") as f:
            f.write(content)
