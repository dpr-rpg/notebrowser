"""Functions for building the site."""
import importlib
import shutil
from pathlib import Path

from notebrowser import assets, rendering
from notebrowser.sitedata import SiteData, create_site_data


def make(base_dir: Path) -> None:
    """Load data, clean site directory, and build site."""
    site_data = create_site_data(base_dir)
    pages = render_pages(site_data)
    clean(site_data)
    write_pages(site_data, pages)
    deploy_fonts(site_data)


def deploy_fonts(site_data: SiteData) -> None:
    """Add font files to site assets."""
    styles = ["regular", "bold", "italic", "bold_italic"]
    target_dir = site_data.site_dir / site_data.asset_dir.relative_to("/")
    for style in styles:
        font_file = f"charter_{style}.woff2"
        font_data = importlib.resources.read_binary(assets, font_file)
        with open(target_dir / font_file, "wb") as new_file:
            new_file.write(font_data)


def clean(site_data: SiteData) -> None:
    """Remove any existing site files."""
    if site_data.site_dir.exists():
        shutil.rmtree(site_data.site_dir)


def render_pages(site_data: SiteData) -> dict[Path, str]:
    """Create page content."""
    stylesheet = (site_data.stylesheet_path, site_data.stylesheet_content)
    homepage = (site_data.homepage, rendering.render_homepage(site_data))
    record_pages = [
        (page, rendering.render_record_page(site_data, uri))
        for uri, page in site_data.record_pages.items()
    ]
    all_pages = [stylesheet, homepage] + record_pages
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
