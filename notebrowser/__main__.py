"""Generate static site from GM notes."""
import os
from pathlib import Path
from sys import argv

from notebrowser.campaigndata import load_campaign_data
from notebrowser.sitedata import create_site_data

base_dir = Path(f"{os.getcwd()}") / Path(argv[1])
assert base_dir.exists()
assert base_dir.is_dir()

site_data = create_site_data(base_dir)
campaign_data = load_campaign_data(base_dir)
site_data.make_directories()
