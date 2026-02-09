.PHONY: test-exports test-presets test-keywords test-get-image-paths test-cli test-edge-cases test

test-exports:
	pytest tests/test_exports.py

test-presets:
	pytest tests/test_presets.py

test-keywords:
	pytest tests/test_keyword_lists.py

test-get-image-paths:
	pytest tests/test_get_image_paths.py

test-cli:
	pytest tests/test_cli.py

test-edge-cases:
	pytest tests/test_edge_cases.py

test:
	pytest
