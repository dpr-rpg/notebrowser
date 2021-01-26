"""Generate static site from GM notes."""
import os
from pathlib import Path
from sys import argv

from notebrowser.campaigndata import load_campaign_data
from notebrowser.rendering import create_record_pages, create_record_toc

base_dir = Path(f"{os.getcwd()}") / Path(argv[1])
assert base_dir.exists()
assert base_dir.is_dir()

site_dir = base_dir / "site"
record_page_dir = site_dir / "records"
record_toc_path = site_dir / "record_toc.html"

site_dir.mkdir(parents=False, exist_ok=True)
record_page_dir.mkdir(parents=False, exist_ok=True)
assert record_page_dir.exists()
assert record_page_dir.is_dir()

campaign_data = load_campaign_data(base_dir)
create_record_pages(campaign_data.records, record_page_dir)
create_record_toc(campaign_data.records, record_toc_path, record_page_dir)
