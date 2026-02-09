"""Test KEYWORD_PRESETS and get_available_presets()."""
import pytest

from parseimagenet import KEYWORD_PRESETS, get_available_presets


def test_available_presets_returns_list():
    """Verify get_available_presets() returns a list."""
    result = get_available_presets()
    assert isinstance(result, list)


def test_available_presets_non_empty():
    """Verify at least one preset is available."""
    assert len(get_available_presets()) > 0


def test_preset_keys_match_available():
    """Verify KEYWORD_PRESETS keys match get_available_presets() output."""
    assert set(KEYWORD_PRESETS.keys()) == set(get_available_presets())


@pytest.mark.parametrize("name", get_available_presets())
def test_preset_value_is_list(name):
    """Verify each preset value is a list."""
    assert isinstance(KEYWORD_PRESETS[name], list), f"Preset '{name}' should be a list"


@pytest.mark.parametrize("name", get_available_presets())
def test_preset_value_is_non_empty(name):
    """Verify each preset contains at least one keyword."""
    assert len(KEYWORD_PRESETS[name]) > 0, f"Preset '{name}' should not be empty"


@pytest.mark.parametrize("name", get_available_presets())
def test_preset_value_contains_only_strings(name):
    """Verify each preset contains only string entries."""
    for entry in KEYWORD_PRESETS[name]:
        assert isinstance(entry, str), f"Preset '{name}' contains non-string: {entry!r}"
