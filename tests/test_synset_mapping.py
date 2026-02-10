"""Tests for the get_synset_mapping() function."""
import pytest
from pathlib import Path

from parseimagenet import get_synset_mapping, get_image_paths_by_keywords
from tests.conftest import MOCK_SYNSET_LINES, WNIDS


# ---------------------------------------------------------------------------
# TestBasicMapping
# ---------------------------------------------------------------------------
class TestBasicMapping:
    """Core behaviour: parsing synset mapping files."""

    def test_returns_dict(self, mock_imagenet):
        result = get_synset_mapping(mock_imagenet)
        assert isinstance(result, dict)

    def test_keys_are_wnid_strings(self, mock_imagenet):
        result = get_synset_mapping(mock_imagenet)
        for key in result:
            assert isinstance(key, str)
            assert key.startswith("n")

    def test_values_are_strings(self, mock_imagenet):
        result = get_synset_mapping(mock_imagenet)
        for value in result.values():
            assert isinstance(value, str)

    def test_correct_count(self, mock_imagenet):
        result = get_synset_mapping(mock_imagenet)
        assert len(result) == 5

    def test_specific_mapping(self, mock_imagenet):
        result = get_synset_mapping(mock_imagenet)
        assert result["n01530575"] == "indigo bunting, indigo bird, indigo finch, Passerina cyanea"
        assert result["n02099601"] == "golden retriever"

    def test_multi_name_categories_preserved(self, mock_imagenet):
        result = get_synset_mapping(mock_imagenet)
        assert ", " in result["n01531178"]
        assert result["n01531178"] == "goldfinch, Carduelis carduelis"


# ---------------------------------------------------------------------------
# TestPathHandling
# ---------------------------------------------------------------------------
class TestPathHandling:
    """Accepts both str and Path base_path."""

    def test_accepts_path_object(self, mock_imagenet):
        result = get_synset_mapping(Path(mock_imagenet))
        assert len(result) == 5

    def test_accepts_string_path(self, mock_imagenet):
        result = get_synset_mapping(str(mock_imagenet))
        assert len(result) == 5


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    """Edge cases: missing files, empty files, malformed lines."""

    def test_missing_file_raises_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            get_synset_mapping(tmp_path)

    def test_empty_file_returns_empty_dict(self, tmp_path):
        (tmp_path / "LOC_synset_mapping.txt").write_text("")
        result = get_synset_mapping(tmp_path)
        assert result == {}

    def test_malformed_lines_no_space_skipped(self, tmp_path):
        (tmp_path / "LOC_synset_mapping.txt").write_text("n00000001\nn00000002 valid category\n")
        result = get_synset_mapping(tmp_path)
        assert "n00000001" not in result
        assert result["n00000002"] == "valid category"

    def test_whitespace_only_lines_skipped(self, tmp_path):
        (tmp_path / "LOC_synset_mapping.txt").write_text("   \n\n\nn01530575 indigo bunting\n")
        result = get_synset_mapping(tmp_path)
        assert len(result) == 1
        assert result["n01530575"] == "indigo bunting"


# ---------------------------------------------------------------------------
# TestConsistencyWithInternal
# ---------------------------------------------------------------------------
class TestConsistencyWithInternal:
    """WNIDs returned by get_image_paths_by_keywords must appear in the mapping."""

    def test_result_wnids_present_in_mapping(self, mock_imagenet):
        mapping = get_synset_mapping(mock_imagenet)
        paths = get_image_paths_by_keywords(mock_imagenet, keywords=["indigo"], num_images=5)
        for p in paths:
            wnid = p.parent.name
            assert wnid in mapping
