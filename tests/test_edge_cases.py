"""Boundary conditions and malformed data."""
from pathlib import Path

import pytest

from parseimagenet import get_image_paths_by_keywords


class TestEmptyFiles:
    """Verify behavior when synset mapping or annotation files are empty."""

    def test_empty_synset_mapping(self, tmp_path):
        """Empty synset mapping means no categories to match."""
        mapping = tmp_path / "LOC_synset_mapping.txt"
        mapping.write_text("")

        imageset_dir = tmp_path / "ILSVRC" / "ImageSets" / "CLS-LOC"
        imageset_dir.mkdir(parents=True)
        (imageset_dir / "train_cls.txt").write_text("n01530575/n01530575_0000 0\n")

        data_dir = tmp_path / "ILSVRC" / "Data" / "CLS-LOC" / "train"
        data_dir.mkdir(parents=True)

        paths = get_image_paths_by_keywords(tmp_path, preset="birds", num_images=10)
        assert paths == []

    def test_empty_train_cls(self, mock_imagenet_empty):
        """Empty train_cls.txt means no annotations, so no images are returned."""
        paths = get_image_paths_by_keywords(mock_imagenet_empty, num_images=10)
        assert paths == []


class TestMalformedData:
    """Verify malformed lines in data files are gracefully skipped."""

    def test_malformed_synset_lines_skipped(self, tmp_path):
        """Lines without a space (no category name) should be skipped."""
        lines = [
            "n01530575 indigo bunting, indigo bird",
            "MALFORMED_NO_SPACE",
            "",
            "n01531178 goldfinch, Carduelis carduelis",
        ]
        mapping = tmp_path / "LOC_synset_mapping.txt"
        mapping.write_text("\n".join(lines) + "\n")

        imageset_dir = tmp_path / "ILSVRC" / "ImageSets" / "CLS-LOC"
        imageset_dir.mkdir(parents=True)
        annotations = [
            "n01530575/n01530575_0000 0",
            "n01531178/n01531178_0000 0",
        ]
        (imageset_dir / "train_cls.txt").write_text("\n".join(annotations) + "\n")

        data_dir = tmp_path / "ILSVRC" / "Data" / "CLS-LOC" / "train"
        data_dir.mkdir(parents=True)

        # Should still find the valid categories
        paths = get_image_paths_by_keywords(tmp_path, keywords=["goldfinch"], num_images=10)
        assert len(paths) == 1

    def test_malformed_annotation_lines_skipped(self, tmp_path):
        """Empty annotation lines should not cause errors."""
        mapping = tmp_path / "LOC_synset_mapping.txt"
        mapping.write_text("n01530575 indigo bunting\n")

        imageset_dir = tmp_path / "ILSVRC" / "ImageSets" / "CLS-LOC"
        imageset_dir.mkdir(parents=True)
        annotations = "n01530575/n01530575_0000 0\n\n\n"
        (imageset_dir / "train_cls.txt").write_text(annotations)

        data_dir = tmp_path / "ILSVRC" / "Data" / "CLS-LOC" / "train"
        data_dir.mkdir(parents=True)

        paths = get_image_paths_by_keywords(tmp_path, keywords=["indigo bunting"], num_images=10)
        assert len(paths) == 1


class TestNumImagesEdgeCases:
    """Verify boundary values for the num_images parameter."""

    def test_num_images_zero_returns_empty(self, mock_imagenet):
        """Requesting zero images returns an empty list."""
        paths = get_image_paths_by_keywords(mock_imagenet, num_images=0)
        assert paths == []

    def test_num_images_one_returns_exactly_one(self, mock_imagenet):
        """Requesting one image returns exactly one result."""
        paths = get_image_paths_by_keywords(mock_imagenet, num_images=1)
        assert len(paths) == 1


class TestDuplicateKeywords:
    """Verify that duplicate keywords do not inflate results."""

    def test_duplicate_keywords_no_double_count(self, mock_imagenet):
        """Passing the same keyword twice should not double the image count."""
        paths_single = get_image_paths_by_keywords(
            mock_imagenet, keywords=["goldfinch"], num_images=999
        )
        paths_double = get_image_paths_by_keywords(
            mock_imagenet, keywords=["goldfinch", "goldfinch"], num_images=999
        )
        assert len(paths_single) == len(paths_double)


class TestMissingFiles:
    """Verify FileNotFoundError is raised when required files are missing."""

    def test_missing_synset_mapping_raises(self, tmp_path):
        """Missing LOC_synset_mapping.txt raises FileNotFoundError."""
        imageset_dir = tmp_path / "ILSVRC" / "ImageSets" / "CLS-LOC"
        imageset_dir.mkdir(parents=True)
        (imageset_dir / "train_cls.txt").write_text("")
        # No LOC_synset_mapping.txt
        with pytest.raises(FileNotFoundError):
            get_image_paths_by_keywords(tmp_path, num_images=10)

    def test_missing_train_cls_raises(self, tmp_path):
        """Missing train_cls.txt raises FileNotFoundError."""
        mapping = tmp_path / "LOC_synset_mapping.txt"
        mapping.write_text("n01530575 indigo bunting\n")
        # No train_cls.txt directory structure
        with pytest.raises(FileNotFoundError):
            get_image_paths_by_keywords(tmp_path, num_images=10)
