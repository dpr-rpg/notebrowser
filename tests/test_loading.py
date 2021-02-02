from pathlib import Path

from notebrowser import loading


def test_load_records():
    loading.load_records(Path("example/records"))
