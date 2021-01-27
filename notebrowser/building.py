"""Functions for building the site."""

import shutil
from pathlib import Path

from notebrowser.campaigndata import CampaignData
from notebrowser.loading import load_campaign_data
from notebrowser.rendering import create_record_pages, create_record_toc
from notebrowser.sitedata import SiteData, create_site_data


def make(base_dir: Path) -> None:
    """Load data, clean site directory, and build site."""
    site_data = create_site_data(base_dir)
    campaign_data = load_campaign_data(base_dir)
    shutil.rmtree(site_data.site_dir)
    build_site(site_data, campaign_data)


def build_site(site_data: SiteData, campaign_data: CampaignData) -> None:
    """Build site."""
    make_directories(site_data)
    make_record_tocs(site_data, campaign_data)
    make_record_pages(site_data, campaign_data)


def make_directories(site_data: SiteData) -> None:
    """Make site directories on the filesystem."""
    site_data.site_dir.mkdir(parents=False, exist_ok=True)
    site_data.record_page_dir.mkdir(parents=False, exist_ok=True)
    site_data.session_page_dir.mkdir(parents=False, exist_ok=True)
    site_data.note_page_dir.mkdir(parents=False, exist_ok=True)


def make_record_tocs(site_data: SiteData, campaign_data: CampaignData) -> None:
    """Make Table of Content page for each RecordType."""
    for rt, record_toc_page in site_data.record_toc_pages.items():
        create_record_toc(
            rt,
            campaign_data.records,
            site_data.record_toc_pages[rt],
            site_data.record_page_dir,
        )


def make_record_pages(site_data: SiteData, campaign_data: CampaignData) -> None:
    """Make a page for each Record."""
    create_record_pages(campaign_data.records, site_data.record_page_dir)
