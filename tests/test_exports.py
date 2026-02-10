"""Verify all public imports work correctly."""
import parseimagenet
import parseimagenet.keywords


def test_package_has_all():
    """Verify the top-level package defines __all__."""
    assert hasattr(parseimagenet, "__all__")


def test_all_names_importable():
    """Verify every name in __all__ is actually importable."""
    for name in parseimagenet.__all__:
        assert hasattr(parseimagenet, name), f"{name} listed in __all__ but not importable"


def test_keywords_has_all():
    """Verify the keywords subpackage defines __all__."""
    assert hasattr(parseimagenet.keywords, "__all__")


def test_keywords_all_names_importable():
    """Verify every name in keywords.__all__ is actually importable."""
    for name in parseimagenet.keywords.__all__:
        obj = getattr(parseimagenet.keywords, name, None)
        assert obj is not None, f"{name} listed in keywords.__all__ but not importable"


def test_keyword_exports_are_lists():
    """Verify every keyword export is a list."""
    for name in parseimagenet.keywords.__all__:
        obj = getattr(parseimagenet.keywords, name)
        assert isinstance(obj, list), f"keywords.{name} should be a list, got {type(obj)}"


def test_keyword_exports_also_on_top_level():
    """Every keyword list in keywords.__all__ should also be re-exported from the top-level package."""
    for name in parseimagenet.keywords.__all__:
        assert hasattr(parseimagenet, name), f"{name} not re-exported from parseimagenet"


def test_get_image_paths_by_keywords_is_callable():
    """Verify get_image_paths_by_keywords is exported and callable."""
    assert callable(parseimagenet.get_image_paths_by_keywords)


def test_get_available_presets_is_callable():
    """Verify get_available_presets is exported and callable."""
    assert callable(parseimagenet.get_available_presets)


def test_get_synset_mapping_is_callable():
    """Verify get_synset_mapping is exported and callable."""
    assert callable(parseimagenet.get_synset_mapping)


def test_keyword_presets_is_dict():
    """Verify KEYWORD_PRESETS is exported as a dict."""
    assert isinstance(parseimagenet.KEYWORD_PRESETS, dict)
