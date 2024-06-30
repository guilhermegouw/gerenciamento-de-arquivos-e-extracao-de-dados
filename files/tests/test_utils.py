import pytest

from files.utils import is_valid_file_name


@pytest.mark.parametrize(
    "file_name, expected",
    [
        ("valid_file_name", True),
        ("valid-file-name", True),
        ("valid_file_name123", True),
        ("invalid@file#name", False),
        ("invalid file name", False),
        ("invalid/file\\name", False),
        ("", False),
    ],
)
def test_is_valid_file_name(file_name, expected):
    assert is_valid_file_name(file_name) == expected
