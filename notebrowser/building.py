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
    # write_stylesheet(site_data)
    write_pages(site_data.site_dir, pages)


def make_directories(site_data: SiteData) -> None:
    """(Re)make site directories on the filesystem."""
    shutil.rmtree(site_data.site_dir)
    site_data.site_dir.mkdir(parents=False, exist_ok=True)
    for d in [site_data.asset_dir, site_data.record_page_dir]:
        (site_data.site_dir / d.relative_to("/")).mkdir(parents=False, exist_ok=True)


# def write_stylesheet(site_data: SiteData) -> None:
#     """Write stylesheet file."""
#     with open(site_data.site_dir / site_data.stylesheet_path, "w") as cssfile:
#         cssfile.write(site_data.stylesheet_content)


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


def write_pages(site_dir: Path, pages: dict[Path, str]) -> None:
    """Apply links and write pages to filesystem."""
    for page, content in pages.items():
        with open(site_dir / page.relative_to("/"), "w") as f:
            f.write(content)
