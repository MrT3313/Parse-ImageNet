"""Test get_image_paths_by_keywords() with argument combinations matching CLI usage."""
import pytest

from parseimagenet import get_image_paths_by_keywords


class TestCLI:
    """Test get_image_paths_by_keywords() with various argument combinations."""

    def test_default_args(self, mock_imagenet):
        """Verify default arguments return a non-empty list."""
        result = get_image_paths_by_keywords(mock_imagenet)
        assert len(result) > 0

    def test_custom_preset(self, mock_imagenet):
        """Verify preset='dogs' returns paths containing the dog WNID."""
        result = get_image_paths_by_keywords(mock_imagenet, preset="dogs", num_images=100)
        wnids_found = {p.parent.name for p in result}
        assert "n02099601" in wnids_found

    def test_custom_keywords(self, mock_imagenet):
        """Verify keywords=['green mamba'] returns paths containing the snake WNID."""
        result = get_image_paths_by_keywords(
            mock_imagenet, keywords=["green mamba"], num_images=100,
        )
        wnids_found = {p.parent.name for p in result}
        assert "n01740131" in wnids_found

    def test_custom_num_images(self, mock_imagenet):
        """Verify num_images=2 returns exactly 2 paths."""
        result = get_image_paths_by_keywords(mock_imagenet, num_images=2)
        assert len(result) == 2

    def test_no_matches(self, mock_imagenet):
        """Verify unrecognized keyword returns an empty list."""
        result = get_image_paths_by_keywords(
            mock_imagenet, keywords=["zzz_nonexistent_zzz"], num_images=100, silent=True,
        )
        assert result == []

    def test_num_images_limits_result(self, mock_imagenet):
        """Verify num_images=3 returns exactly 3 paths."""
        result = get_image_paths_by_keywords(mock_imagenet, num_images=3)
        assert len(result) == 3

    def test_source_val(self, mock_imagenet):
        """Verify source='val' returns paths under the val directory."""
        result = get_image_paths_by_keywords(mock_imagenet, source="val", num_images=5)
        val_dir = mock_imagenet / "ILSVRC" / "Data" / "CLS-LOC" / "val"
        for p in result:
            assert str(p).startswith(str(val_dir))
