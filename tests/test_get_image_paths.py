"""Core tests for get_image_paths_by_keywords()."""
import random
from pathlib import Path

import pytest

from parseimagenet import get_image_paths_by_keywords


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

class TestInputValidation:
    """Verify type and value checks on function arguments."""

    def test_string_keywords_raises_type_error(self, mock_imagenet):
        """Passing a bare string instead of a list raises TypeError."""
        with pytest.raises(TypeError, match="list of strings"):
            get_image_paths_by_keywords(mock_imagenet, keywords="golden retriever")

    def test_tuple_keywords_raises_type_error(self, mock_imagenet):
        """Passing a tuple instead of a list raises TypeError."""
        with pytest.raises(TypeError, match="list of strings"):
            get_image_paths_by_keywords(mock_imagenet, keywords=("golden retriever",))

    def test_int_keywords_raises_type_error(self, mock_imagenet):
        """Passing an int instead of a list raises TypeError."""
        with pytest.raises(TypeError, match="list of strings"):
            get_image_paths_by_keywords(mock_imagenet, keywords=42)

    def test_invalid_preset_raises_value_error(self, mock_imagenet):
        """An unrecognized preset name raises ValueError."""
        with pytest.raises(ValueError, match="Unknown preset"):
            get_image_paths_by_keywords(mock_imagenet, preset="nonexistent")


# ---------------------------------------------------------------------------
# Preset selection
# ---------------------------------------------------------------------------

class TestPresetSelection:
    """Verify built-in presets select the correct categories."""

    def test_default_preset_is_birds(self, mock_imagenet):
        """Default preset='birds' should match our bird mock categories."""
        paths = get_image_paths_by_keywords(mock_imagenet, num_images=100)
        # Should match indigo bunting (n01530575) and goldfinch (n01531178)
        wnids_found = {p.parent.name for p in paths}
        assert "n01530575" in wnids_found or "n01531178" in wnids_found

    def test_dogs_preset_matches_retriever(self, mock_imagenet):
        """The 'dogs' preset matches the golden retriever category."""
        paths = get_image_paths_by_keywords(mock_imagenet, preset="dogs", num_images=100)
        wnids_found = {p.parent.name for p in paths}
        assert "n02099601" in wnids_found

    def test_snakes_preset_matches_green_mamba(self, mock_imagenet):
        """The 'snakes' preset matches the green mamba category."""
        paths = get_image_paths_by_keywords(mock_imagenet, preset="snakes", num_images=100)
        wnids_found = {p.parent.name for p in paths}
        assert "n01740131" in wnids_found


# ---------------------------------------------------------------------------
# Custom keywords
# ---------------------------------------------------------------------------

class TestCustomKeywords:
    """Verify custom keyword lists filter categories correctly."""

    def test_custom_keywords_override_preset(self, mock_imagenet):
        """Explicit keywords take precedence over the preset."""
        paths = get_image_paths_by_keywords(
            mock_imagenet, preset="birds", keywords=["golden retriever"], num_images=100
        )
        wnids_found = {p.parent.name for p in paths}
        assert "n02099601" in wnids_found
        # Should NOT contain bird categories
        assert "n01530575" not in wnids_found
        assert "n01531178" not in wnids_found

    def test_empty_keyword_list_returns_empty(self, mock_imagenet):
        """An empty keyword list matches nothing and returns []."""
        paths = get_image_paths_by_keywords(mock_imagenet, keywords=[], num_images=100)
        assert paths == []

    def test_single_keyword_matches(self, mock_imagenet):
        """A single matching keyword returns images from its category."""
        paths = get_image_paths_by_keywords(
            mock_imagenet, keywords=["goldfinch"], num_images=100
        )
        assert len(paths) > 0
        wnids_found = {p.parent.name for p in paths}
        assert "n01531178" in wnids_found


# ---------------------------------------------------------------------------
# Return values
# ---------------------------------------------------------------------------

class TestReturnValues:
    """Verify the type and structure of returned paths."""

    def test_returns_list(self, mock_imagenet):
        """The return value is a list."""
        result = get_image_paths_by_keywords(mock_imagenet, num_images=5)
        assert isinstance(result, list)

    def test_returns_path_objects(self, mock_imagenet):
        """Each element in the result is a Path object."""
        result = get_image_paths_by_keywords(mock_imagenet, num_images=5)
        for p in result:
            assert isinstance(p, Path)

    def test_paths_end_in_jpeg(self, mock_imagenet):
        """All returned paths have a .JPEG extension."""
        result = get_image_paths_by_keywords(mock_imagenet, num_images=5)
        for p in result:
            assert p.suffix == ".JPEG"

    def test_paths_are_under_data_dir(self, mock_imagenet):
        """All returned paths are under the ILSVRC train data directory."""
        result = get_image_paths_by_keywords(mock_imagenet, num_images=5)
        data_dir = mock_imagenet / "ILSVRC" / "Data" / "CLS-LOC" / "train"
        for p in result:
            assert str(p).startswith(str(data_dir))


# ---------------------------------------------------------------------------
# Sampling / num_images
# ---------------------------------------------------------------------------

class TestSampling:
    """Verify num_images sampling and determinism."""

    def test_num_images_caps_results(self, mock_imagenet):
        """Requesting fewer images than available returns exactly that many."""
        paths = get_image_paths_by_keywords(mock_imagenet, num_images=3)
        assert len(paths) == 3

    def test_requesting_more_than_available_returns_all(self, mock_imagenet):
        """Requesting more images than available returns all of them."""
        # Birds preset matches 2 categories x 5 images = 10 images
        paths = get_image_paths_by_keywords(mock_imagenet, num_images=999)
        assert len(paths) == 10

    def test_deterministic_with_seed(self, mock_imagenet):
        """Setting the same random seed produces identical results."""
        random.seed(42)
        paths1 = get_image_paths_by_keywords(mock_imagenet, num_images=5)
        random.seed(42)
        paths2 = get_image_paths_by_keywords(mock_imagenet, num_images=5)
        assert paths1 == paths2

    def test_num_images_1_returns_exactly_1(self, mock_imagenet):
        """Requesting exactly one image returns a single-element list."""
        paths = get_image_paths_by_keywords(mock_imagenet, num_images=1)
        assert len(paths) == 1


# ---------------------------------------------------------------------------
# File verification
# ---------------------------------------------------------------------------

class TestFileVerification:
    """Verify file-existence checking and verification output."""

    def test_returns_paths_when_files_missing(self, mock_imagenet_no_files, capsys):
        """Paths are returned even when the JPEG files do not exist on disk."""
        paths = get_image_paths_by_keywords(mock_imagenet_no_files, num_images=5)
        assert len(paths) == 5
        captured = capsys.readouterr()
        assert "Verified 0/" in captured.out

    def test_verified_count_when_files_exist(self, mock_imagenet, capsys):
        """When files exist on disk, the verified count matches the total."""
        paths = get_image_paths_by_keywords(mock_imagenet, num_images=5)
        assert len(paths) == 5
        captured = capsys.readouterr()
        assert "Verified 5/5" in captured.out


# ---------------------------------------------------------------------------
# No matches
# ---------------------------------------------------------------------------

class TestNoMatches:
    """Verify behavior when no categories match the keywords."""

    def test_unrecognized_keyword_returns_empty(self, mock_imagenet, capsys):
        """A keyword that matches no category returns [] and prints a message."""
        paths = get_image_paths_by_keywords(
            mock_imagenet, keywords=["zzz_nonexistent_zzz"], num_images=100
        )
        assert paths == []
        captured = capsys.readouterr()
        assert "No matching images found!" in captured.out

    def test_empty_annotations_returns_empty(self, mock_imagenet_empty, capsys):
        """Empty annotations file returns [] and prints a message."""
        paths = get_image_paths_by_keywords(mock_imagenet_empty, num_images=100)
        assert paths == []
        captured = capsys.readouterr()
        assert "No matching images found!" in captured.out


# ---------------------------------------------------------------------------
# Print output
# ---------------------------------------------------------------------------

class TestPrintOutput:
    """Verify informational messages printed to stdout."""

    def test_prints_loading_message(self, mock_imagenet, capsys):
        """The 'Loading category names...' message is printed."""
        get_image_paths_by_keywords(mock_imagenet, num_images=5)
        captured = capsys.readouterr()
        assert "Loading category names..." in captured.out

    def test_prints_searching_message(self, mock_imagenet, capsys):
        """The 'SEARCHING WITH KEYWORDS' banner is printed."""
        get_image_paths_by_keywords(mock_imagenet, num_images=5)
        captured = capsys.readouterr()
        assert "SEARCHING WITH KEYWORDS" in captured.out

    def test_prints_selected_count(self, mock_imagenet, capsys):
        """The 'Selected N random images' count is printed."""
        get_image_paths_by_keywords(mock_imagenet, num_images=3)
        captured = capsys.readouterr()
        assert "Selected 3 random images" in captured.out

    def test_prints_category_count(self, mock_imagenet, capsys):
        """The 'Total matching categories' count is printed."""
        get_image_paths_by_keywords(mock_imagenet, num_images=5)
        captured = capsys.readouterr()
        assert "Total matching categories:" in captured.out
