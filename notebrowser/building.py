"""Functions for building the site."""

import shutil
from pathlib import Path

from notebrowser import rendering
from notebrowser.sitedata import SiteData, create_site_data


def make(base_dir: Path) -> None:
    """Load data, clean site directory, and build site."""
    site_data = create_site_data(base_dir)
    pages = render_pages(site_data)
    make_directories(site_data)
    write_pages(pages)


def make_directories(site_data: SiteData) -> None:
    """(Re)make site directories on the filesystem."""
    shutil.rmtree(site_data.site_dir)
    site_data.site_dir.mkdir(parents=False, exist_ok=True)
    site_data.record_page_dir.mkdir(parents=False, exist_ok=True)


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


def write_pages(pages: dict[Path, str]) -> None:
    """Apply links and write pages to filesystem."""
    for page, content in pages.items():
        with open(page, "w") as f:
            f.write(content)
