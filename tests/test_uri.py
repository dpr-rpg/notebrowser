from notebrowser import uri


def test_get_references():
    assert uri.get_references("{test1} _{test2}_. {test1}") == set(["test1", "test2"])
