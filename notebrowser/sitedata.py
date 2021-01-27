"""Classes and functions for building the site."""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from notebrowser.campaigndata import CampaignData
from notebrowser.loading import load_campaign_data
from notebrowser.records import RecordType
from notebrowser.rendering import create_record_pages, create_record_toc


@dataclass(frozen=True)
class SiteData:
    """Container for site data."""

    campaign_data: CampaignData

    site_dir: Path
    record_page_dir: Path
    session_page_dir: Path
    note_page_dir: Path

    home_page: Path
    session_log_page: Path
    note_toc_page: Path
    record_toc_pages: Dict[RecordType, Path]

    def make_directories(self) -> None:
        """Make site directories on the filesystem."""
        self.site_dir.mkdir(parents=False, exist_ok=True)
        self.record_page_dir.mkdir(parents=False, exist_ok=True)
        self.session_page_dir.mkdir(parents=False, exist_ok=True)
        self.note_page_dir.mkdir(parents=False, exist_ok=True)

    def make_record_tocs(self) -> None:
        """Make Table of Content page for each RecordType."""
        for rt, record_toc_page in self.record_toc_pages.items():
            create_record_toc(
                rt,
                self.campaign_data.records,
                self.record_toc_pages[rt],
                self.record_page_dir,
            )

    def make_record_pages(self) -> None:
        """Make a page for each Record."""
        create_record_pages(self.campaign_data.records, self.record_page_dir)


def create_site_data(base_dir: Path) -> SiteData:
    """Create site SiteData."""
    campaign_data = load_campaign_data(base_dir)
    site_dir = base_dir / "site"
    return SiteData(
        campaign_data,
        site_dir,
        site_dir / "records",
        site_dir / "sessions",
        site_dir / "notes",
        site_dir / "home.html",
        site_dir / "session_log.html",
        site_dir / "note_toc.html",
        {rt: site_dir / f"{rt.value}_toc.html" for rt in RecordType},
    )
