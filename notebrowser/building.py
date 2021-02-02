"""Functions for building the site."""

import shutil
from pathlib import Path

from notebrowser import rendering
from notebrowser.sitedata import SiteData, create_site_data


def make(base_dir: Path) -> None:
    """Load data, clean site directory, and build site."""
    site_data = create_site_data(base_dir)
    shutil.rmtree(site_data.site_dir)
    build_site(site_data)


def build_site(site_data: SiteData) -> None:
    """Build site."""
    make_directories(site_data)
    make_homepage(site_data)
    make_record_pages(site_data)


def make_directories(site_data: SiteData) -> None:
    """Make site directories on the filesystem."""
    site_data.site_dir.mkdir(parents=False, exist_ok=True)
    site_data.record_page_dir.mkdir(parents=False, exist_ok=True)


def make_homepage(site_data: SiteData) -> None:
    """Make site homepage."""
    with open(site_data.homepage, "w") as homepage:
        homepage.write(
            rendering.render_homepage(site_data),
        )


def make_record_pages(site_data: SiteData) -> None:
    """Make a page for each Record."""
    for uri in site_data.records:
        with open(site_data.record_pages[uri], "w") as recordpage:
            recordpage.write(rendering.render_record_page(site_data, uri))
