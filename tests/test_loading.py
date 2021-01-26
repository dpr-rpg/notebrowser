from pathlib import Path

from notebrowser.campaigndata import load_notes, load_records, load_sessions
from notebrowser.records import get_references


def test_load_records():
    load_records(Path("example/records"))


def test_load_notes():
    load_notes(Path("example/notes"))


def test_load_sessions():
    load_sessions(Path("example/sessions"))


def test_get_references():
    assert get_references("{test1} _{test2}_. {test1}") == set(["test1", "test2"])
