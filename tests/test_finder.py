import pytest
from orca.finder import find_filepath


@pytest.mark.parametrize(
    "unique_id, expected",
    [
        ("unique_id_0", "data_file_0"),
        ("unique_id_1", "data_file_1"),
        ("unique_id_2", "data_file_2"),
    ],
)
def test_find_filepath(test_session, unique_id, expected):
    filename = find_filepath(test_session, unique_id)
    assert filename == expected


@pytest.mark.parametrize(
    "bad_unique_id",
    [
        (0),  # search expects a string so an int will break it
    ],
)
def test_find_filepath_bad_search(test_session, bad_unique_id):
    with pytest.raises(Exception):
        filename = find_filepath(test_session, bad_unique_id)


@pytest.mark.parametrize(
    "no_match_id",
    [
        ("no_match_id"),
    ],
)
def test_find_filepath_no_match(test_session, no_match_id):
    with pytest.raises(Exception):
        filename = find_filepath(test_session, no_match_id)
