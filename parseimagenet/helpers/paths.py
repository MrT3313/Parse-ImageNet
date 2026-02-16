from pathlib import Path


def resolve_paths(base_path, source):
    """Return (annotations_file, data_path) for the given split.

    Args:
        base_path: Path to ImageNet-Subset directory (str or Path).
        source: "train" or "val".

    Returns:
        Tuple of (annotations_file, data_path) as Path objects.
    """
    base = Path(base_path)
    return (
        _resolve_annotation_path(base, source),
        _resolve_data_path(base, source),
    )


def _resolve_annotation_path(base_path, source):
    if source == "train":
        return base_path / "ILSVRC" / "ImageSets" / "CLS-LOC" / "train_cls.txt"
    return base_path / "ILSVRC" / "ImageSets" / "CLS-LOC" / "val.txt"


def _resolve_data_path(base_path, source):
    if source == "train":
        return base_path / "ILSVRC" / "Data" / "CLS-LOC" / "train"
    return base_path / "ILSVRC" / "Data" / "CLS-LOC" / "val"
