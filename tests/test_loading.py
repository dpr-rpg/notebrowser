from pathlib import Path

from notebrowser import loading
from notebrowser.uri import URI


def test_load_records():
    records = loading.load_records(Path("example/records"))
    assert len(records) == 5
    assert records[URI("loc")].name == "Place"
    assert (
        records[URI("session-01")].text_body
        == "This was a really exciting session. {player1} and {player2} went to {loc}."
    )
