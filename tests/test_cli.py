"""Test the CLI main() function."""
import sys

import pytest

from parseimagenet.ParseImageNetSubset import main


class TestCLI:
    """Test the CLI main() entry point with various argument combinations."""

    def test_default_args(self, mock_imagenet, monkeypatch, capsys):
        """Verify CLI runs successfully with no optional arguments."""
        monkeypatch.setattr(sys, "argv", [
            "parseimagenet", "--base_path", str(mock_imagenet),
        ])
        main()
        captured = capsys.readouterr()
        assert "First 10 image paths:" in captured.out

    def test_custom_preset(self, mock_imagenet, monkeypatch, capsys):
        """Verify --preset flag selects the correct category."""
        monkeypatch.setattr(sys, "argv", [
            "parseimagenet", "--base_path", str(mock_imagenet),
            "--preset", "dogs",
        ])
        main()
        captured = capsys.readouterr()
        assert "golden retriever" in captured.out

    def test_custom_keywords(self, mock_imagenet, monkeypatch, capsys):
        """Verify --keywords flag filters by custom keyword."""
        monkeypatch.setattr(sys, "argv", [
            "parseimagenet", "--base_path", str(mock_imagenet),
            "--keywords", "green mamba",
        ])
        main()
        captured = capsys.readouterr()
        assert "First 10 image paths:" in captured.out

    def test_custom_num_images(self, mock_imagenet, monkeypatch, capsys):
        """Verify --num_images flag limits the number of selected images."""
        monkeypatch.setattr(sys, "argv", [
            "parseimagenet", "--base_path", str(mock_imagenet),
            "--num_images", "2",
        ])
        main()
        captured = capsys.readouterr()
        assert "Selected 2 random images" in captured.out

    def test_no_matches_cli(self, mock_imagenet, monkeypatch, capsys):
        """Verify CLI prints 'No matching images found!' when keywords match nothing."""
        monkeypatch.setattr(sys, "argv", [
            "parseimagenet", "--base_path", str(mock_imagenet),
            "--keywords", "zzz_nonexistent_zzz",
        ])
        main()
        captured = capsys.readouterr()
        assert "No matching images found!" in captured.out
        assert "First 10 image paths:" not in captured.out

    def test_num_images_flag_limits_output(self, mock_imagenet, monkeypatch, capsys):
        """Verify output message reflects the requested image count."""
        monkeypatch.setattr(sys, "argv", [
            "parseimagenet", "--base_path", str(mock_imagenet),
            "--num_images", "3",
        ])
        main()
        captured = capsys.readouterr()
        assert "Selected 3 random images" in captured.out
