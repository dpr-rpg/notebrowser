"""Functions for building the site."""

import shutil
from pathlib import Path

from notebrowser import rendering
from notebrowser.loading import load_records
from notebrowser.records import Record
from notebrowser.sitedata import SiteData, create_site_data
from notebrowser.uri import Library


def make(base_dir: Path) -> None:
    """Load data, clean site directory, and build site."""
    site_data = create_site_data(base_dir)
    records = load_records(base_dir)
    shutil.rmtree(site_data.site_dir)
    build_site(site_data, records)


def build_site(site_data: SiteData, records: Library[Record]) -> None:
    """Build site."""
    make_directories(site_data)
    make_record_pages(site_data, records)


def make_directories(site_data: SiteData) -> None:
    """Make site directories on the filesystem."""
    site_data.site_dir.mkdir(parents=False, exist_ok=True)
    site_data.record_page_dir.mkdir(parents=False, exist_ok=True)
    site_data.session_page_dir.mkdir(parents=False, exist_ok=True)
    site_data.note_page_dir.mkdir(parents=False, exist_ok=True)


def make_record_pages(site_data: SiteData, records: Library[Record]) -> None:
    """Make a page for each Record."""
    rendering.create_record_pages(records, site_data.record_page_dir)
