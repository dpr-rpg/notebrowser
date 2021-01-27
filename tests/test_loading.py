from pathlib import Path

from notebrowser.campaigndata import load_campaign_data
from notebrowser.uri import get_references


def test_load_campaign_data():
    load_campaign_data(Path("example"))


def test_get_references():
    assert get_references("{test1} _{test2}_. {test1}") == set(["test1", "test2"])
