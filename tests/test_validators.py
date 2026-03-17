import pytest
from utils.validation import validate_profile_data

@pytest.mark.parametrize("first, last, sid, expected",
    [
        # Valid partition
        ("Alice", "Smith", "12345678", None),
        # Missing first_name
        ("", "Smith", "12345678", "All fields are required."),
        # Missing last_name
        ("Alice", "", "12345678", "All fields are required."),
        # Missing student_id
        ("Alice", "Smith", "", "All fields are required."),
        # None value
        (None, "Smith", "12345678", "All fields are required."),
        # All empty
        ("", "", "", "All fields are required."),
    ]
)
def test_validate(first, last, sid, expected):
    assert validate_profile_data(first, last, sid) == expected