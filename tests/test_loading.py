from pathlib import Path

from notebrowser import loading


def test_load_campaign_data():
    loading.load_campaign_data(Path("example"))
