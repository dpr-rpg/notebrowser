from pathlib import Path

from notebrowser.campaigndata import Note, Session, load_from_markdown, load_records
from notebrowser.uri import get_references


def test_load_records():
    load_records(Path("example/records"))


def test_load_notes():
    load_from_markdown(Path("example/notes"), Note)


def test_load_sessions():
    load_from_markdown(Path("example/sessions"), Session)


def test_get_references():
    assert get_references("{test1} _{test2}_. {test1}") == set(["test1", "test2"])
