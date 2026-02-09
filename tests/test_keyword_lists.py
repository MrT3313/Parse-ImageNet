"""Validate keyword list contents: non-empty, all strings, no whitespace issues."""
import pytest
import parseimagenet.keywords

# Dynamically build the list of keyword lists from the keywords subpackage __all__
ALL_LISTS = {
    name: getattr(parseimagenet.keywords, name)
    for name in parseimagenet.keywords.__all__
}


@pytest.mark.parametrize("name,kw_list", list(ALL_LISTS.items()))
def test_list_is_non_empty(name, kw_list):
    """Verify each keyword list contains at least one entry."""
    assert len(kw_list) > 0, f"{name} should not be empty"


@pytest.mark.parametrize("name,kw_list", list(ALL_LISTS.items()))
def test_all_entries_are_strings(name, kw_list):
    """Verify every entry in the keyword list is a string."""
    for entry in kw_list:
        assert isinstance(entry, str), f"{name} contains non-string: {entry!r}"


@pytest.mark.parametrize("name,kw_list", list(ALL_LISTS.items()))
def test_no_empty_strings(name, kw_list):
    """Verify no keyword list contains empty strings."""
    for entry in kw_list:
        assert entry != "", f"{name} contains an empty string"


@pytest.mark.parametrize("name,kw_list", list(ALL_LISTS.items()))
def test_no_leading_trailing_whitespace(name, kw_list):
    """Verify no keyword has leading or trailing whitespace."""
    for entry in kw_list:
        assert entry == entry.strip(), f"{name} entry has whitespace issues: {entry!r}"


@pytest.mark.parametrize("name,kw_list", list(ALL_LISTS.items()))
def test_minimum_entry_count(name, kw_list):
    """Every keyword list should have at least 5 entries."""
    assert len(kw_list) >= 5, f"{name} has only {len(kw_list)} entries, expected at least 5"


# ------------------------------------------------------------------
# Spot-checks: regression guards for known entries.
# These are intentionally static per-list.
# ------------------------------------------------------------------

def test_bird_breeds_contains_albatross():
    """Spot-check that 'albatross' is in the bird breeds list."""
    assert "albatross" in parseimagenet.keywords.bird_breeds


def test_dog_breeds_contains_golden_retriever():
    """Spot-check that 'golden retriever' is in the dog breeds list."""
    assert "golden retriever" in parseimagenet.keywords.dog_breeds


def test_snake_breeds_contains_green_mamba():
    """Spot-check that 'green mamba' is in the snake breeds list."""
    assert "green mamba" in parseimagenet.keywords.snake_breeds
