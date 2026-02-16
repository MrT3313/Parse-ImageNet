"""Tests for the source parameter of get_image_paths_by_keywords()."""
import random
from pathlib import Path

import pytest

from parseimagenet import get_image_paths_by_keywords


# ---------------------------------------------------------------------------
# Source validation
# ---------------------------------------------------------------------------

class TestSourceValidation:
    """Verify source parameter validation."""

    def test_invalid_source_raises_value_error(self, mock_imagenet):
        """An unrecognized source raises ValueError."""
        with pytest.raises(ValueError, match="Unknown source"):
            get_image_paths_by_keywords(mock_imagenet, source="test")

    def test_default_source_is_train(self, mock_imagenet):
        """Omitting source defaults to train (paths under train/ dir)."""
        paths = get_image_paths_by_keywords(mock_imagenet, num_images=5)
        train_dir = mock_imagenet / "ILSVRC" / "Data" / "CLS-LOC" / "train"
        for p in paths:
            assert str(p).startswith(str(train_dir))


# ---------------------------------------------------------------------------
# Val basics
# ---------------------------------------------------------------------------

class TestValBasics:
    """Verify basic val source behavior."""

    def test_val_returns_paths(self, mock_imagenet):
        """Val source returns a non-empty list."""
        paths = get_image_paths_by_keywords(mock_imagenet, source="val", num_images=5)
        assert len(paths) > 0

    def test_val_returns_path_objects(self, mock_imagenet):
        """Each element returned for val is a Path object."""
        paths = get_image_paths_by_keywords(mock_imagenet, source="val", num_images=5)
        for p in paths:
            assert isinstance(p, Path)

    def test_val_paths_end_in_jpeg(self, mock_imagenet):
        """All val paths have a .JPEG extension."""
        paths = get_image_paths_by_keywords(mock_imagenet, source="val", num_images=5)
        for p in paths:
            assert p.suffix == ".JPEG"

    def test_val_paths_are_under_val_dir(self, mock_imagenet):
        """All val paths are under the ILSVRC val data directory, not train."""
        paths = get_image_paths_by_keywords(mock_imagenet, source="val", num_images=5)
        val_dir = mock_imagenet / "ILSVRC" / "Data" / "CLS-LOC" / "val"
        train_dir = mock_imagenet / "ILSVRC" / "Data" / "CLS-LOC" / "train"
        for p in paths:
            assert str(p).startswith(str(val_dir))
            assert not str(p).startswith(str(train_dir))

    def test_val_paths_are_flat(self, mock_imagenet):
        """Val paths have flat structure (no wnid subdirectory)."""
        paths = get_image_paths_by_keywords(mock_imagenet, source="val", num_images=5)
        val_dir = mock_imagenet / "ILSVRC" / "Data" / "CLS-LOC" / "val"
        for p in paths:
            assert p.parent == val_dir

    def test_val_files_exist(self, mock_imagenet):
        """Val JPEG files actually exist on disk."""
        paths = get_image_paths_by_keywords(mock_imagenet, source="val", num_images=5)
        for p in paths:
            assert p.exists()


# ---------------------------------------------------------------------------
# Val keyword filtering
# ---------------------------------------------------------------------------

class TestValKeywordFiltering:
    """Verify keyword/preset filtering works with val source."""

    def test_val_birds_preset(self, mock_imagenet):
        """Birds preset with val source returns bird images."""
        paths = get_image_paths_by_keywords(
            mock_imagenet, preset="birds", source="val", num_images=100
        )
        assert len(paths) == 10  # 2 bird wnids x 5 images each

    def test_val_dogs_preset(self, mock_imagenet):
        """Dogs preset with val source returns dog images."""
        paths = get_image_paths_by_keywords(
            mock_imagenet, preset="dogs", source="val", num_images=100
        )
        assert len(paths) == 5  # 1 dog wnid x 5 images

    def test_val_custom_keywords(self, mock_imagenet):
        """Custom keywords work with val source."""
        paths = get_image_paths_by_keywords(
            mock_imagenet, keywords=["green mamba"], source="val", num_images=100
        )
        assert len(paths) == 5

    def test_val_no_match_returns_empty(self, mock_imagenet):
        """Keywords matching nothing return [] for val source."""
        paths = get_image_paths_by_keywords(
            mock_imagenet, keywords=["zzz_nonexistent_zzz"], source="val", num_images=100
        )
        assert paths == []


# ---------------------------------------------------------------------------
# Val sampling
# ---------------------------------------------------------------------------

class TestValSampling:
    """Verify num_images sampling with val source."""

    def test_val_num_images_caps_results(self, mock_imagenet):
        """Requesting fewer images than available returns exactly that many."""
        paths = get_image_paths_by_keywords(
            mock_imagenet, source="val", num_images=3
        )
        assert len(paths) == 3

    def test_val_requesting_more_than_available_returns_all(self, mock_imagenet):
        """Requesting more images than available returns all of them."""
        paths = get_image_paths_by_keywords(
            mock_imagenet, source="val", num_images=999
        )
        # Birds preset: 2 wnids x 5 images = 10
        assert len(paths) == 10

    def test_val_deterministic_with_seed(self, mock_imagenet):
        """Setting the same random seed produces identical val results."""
        random.seed(42)
        paths1 = get_image_paths_by_keywords(mock_imagenet, source="val", num_images=5)
        random.seed(42)
        paths2 = get_image_paths_by_keywords(mock_imagenet, source="val", num_images=5)
        assert paths1 == paths2


# ---------------------------------------------------------------------------
# Val print output
# ---------------------------------------------------------------------------

class TestValPrintOutput:
    """Verify informational messages for val source."""

    def test_val_prints_val_annotations_message(self, mock_imagenet, capsys):
        """Val source prints 'Parsing val annotations...', not 'training'."""
        get_image_paths_by_keywords(
            mock_imagenet, source="val", num_images=5, silent=False
        )
        captured = capsys.readouterr()
        assert "Parsing val annotations..." in captured.out
        assert "Parsing train annotations..." not in captured.out

    def test_train_prints_train_annotations_message(self, mock_imagenet, capsys):
        """Train source prints 'Parsing train annotations...'."""
        get_image_paths_by_keywords(
            mock_imagenet, source="train", num_images=5, silent=False
        )
        captured = capsys.readouterr()
        assert "Parsing train annotations..." in captured.out


# ---------------------------------------------------------------------------
# Val edge cases
# ---------------------------------------------------------------------------

class TestValEdgeCases:
    """Verify edge cases for val source."""

    def test_val_empty_annotations_returns_empty(self, mock_imagenet_empty):
        """Empty val.txt returns []."""
        paths = get_image_paths_by_keywords(
            mock_imagenet_empty, source="val", num_images=100
        )
        assert paths == []

    def test_val_missing_solution_csv_raises(self, mock_imagenet, tmp_path):
        """Missing LOC_val_solution.csv raises FileNotFoundError."""
        # Remove the solution file
        (mock_imagenet / "LOC_val_solution.csv").unlink()
        with pytest.raises(FileNotFoundError):
            get_image_paths_by_keywords(mock_imagenet, source="val", num_images=5)

    def test_val_missing_val_txt_raises(self, mock_imagenet):
        """Missing val.txt raises FileNotFoundError."""
        (mock_imagenet / "ILSVRC" / "ImageSets" / "CLS-LOC" / "val.txt").unlink()
        with pytest.raises(FileNotFoundError):
            get_image_paths_by_keywords(mock_imagenet, source="val", num_images=5)

    def test_val_num_images_zero_returns_empty(self, mock_imagenet):
        """num_images=0 with val source returns []."""
        paths = get_image_paths_by_keywords(
            mock_imagenet, source="val", num_images=0
        )
        assert paths == []

    def test_val_images_not_in_solution_csv_skipped(self, tmp_path):
        """Images in val.txt but not in LOC_val_solution.csv are silently skipped."""
        from tests.conftest import MOCK_SYNSET_LINES

        # Minimal setup with a val image not in solution CSV
        base = tmp_path
        (base / "LOC_synset_mapping.txt").write_text("\n".join(MOCK_SYNSET_LINES) + "\n")

        imageset_dir = base / "ILSVRC" / "ImageSets" / "CLS-LOC"
        imageset_dir.mkdir(parents=True, exist_ok=True)

        val_data_dir = base / "ILSVRC" / "Data" / "CLS-LOC" / "val"
        val_data_dir.mkdir(parents=True, exist_ok=True)

        # val.txt has an image, but solution CSV has no entry for it
        (imageset_dir / "val.txt").write_text("ILSVRC2012_val_00099999 1\n")
        (base / "LOC_val_solution.csv").write_text("ImageId,PredictionString\n")

        paths = get_image_paths_by_keywords(base, source="val", num_images=100)
        assert paths == []
