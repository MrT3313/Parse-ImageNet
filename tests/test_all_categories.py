"""Tests for all-categories mode (preset=None, keywords=None)."""
import pytest

from parseimagenet.ParseImageNetSubset import get_image_paths_by_keywords


class TestAllCategoriesMode:
    """Verify that preset=None with keywords=None returns images from all categories."""

    def test_returns_images_from_all_categories(self, mock_imagenet):
        """preset=None should return images drawn from all 5 WNIDs (25 total)."""
        result = get_image_paths_by_keywords(
            mock_imagenet, preset=None, keywords=None, num_images=25,
        )
        assert len(result) == 25

    def test_num_images_caps_selection(self, mock_imagenet):
        """num_images should cap the returned count even in all-categories mode."""
        result = get_image_paths_by_keywords(
            mock_imagenet, preset=None, keywords=None, num_images=3,
        )
        assert len(result) == 3

    def test_num_images_zero_returns_empty(self, mock_imagenet):
        """num_images=0 should return an empty list."""
        result = get_image_paths_by_keywords(
            mock_imagenet, preset=None, keywords=None, num_images=0,
        )
        assert result == []

    def test_keywords_override_preset_none(self, mock_imagenet):
        """Explicit keywords should still work when preset=None."""
        result = get_image_paths_by_keywords(
            mock_imagenet, preset=None, keywords=["golden retriever"], num_images=50,
        )
        assert len(result) == 5
        assert all("n02099601" in str(p) for p in result)

    def test_source_val(self, mock_imagenet):
        """All-categories mode should work with source='val'."""
        result = get_image_paths_by_keywords(
            mock_imagenet, preset=None, keywords=None, num_images=25, source="val",
        )
        assert len(result) == 25
        assert all("val" in str(p) for p in result)

    def test_empty_annotations_returns_empty(self, mock_imagenet_empty):
        """All-categories mode with empty annotations should return []."""
        result = get_image_paths_by_keywords(
            mock_imagenet_empty, preset=None, keywords=None, num_images=10,
        )
        assert result == []


class TestPresetNone:
    """Verify preset=None triggers all-categories mode."""

    def test_preset_none_returns_all_wnids(self, mock_imagenet):
        """preset=None should return images from all 5 WNIDs."""
        result = get_image_paths_by_keywords(
            mock_imagenet, preset=None, keywords=None, num_images=25,
        )
        wnids_found = {p.parent.name for p in result}
        assert len(wnids_found) == 5
