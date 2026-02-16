import pytest
from pathlib import Path


# Synset mapping entries for mock data
MOCK_SYNSET_LINES = [
    "n01530575 indigo bunting, indigo bird, indigo finch, Passerina cyanea",
    "n01531178 goldfinch, Carduelis carduelis",
    "n02099601 golden retriever",
    "n01740131 green mamba",
    "n99999999 imaginary creature, no match",
]

# WNIDs used in mock data
WNIDS = ["n01530575", "n01531178", "n02099601", "n01740131", "n99999999"]


def _build_mock_imagenet(tmp_path, synset_lines=None, annotation_wnids=None, create_jpegs=True):
    """Build a mock ImageNet directory structure under tmp_path."""
    if synset_lines is None:
        synset_lines = MOCK_SYNSET_LINES
    if annotation_wnids is None:
        annotation_wnids = WNIDS

    # LOC_synset_mapping.txt
    mapping_file = tmp_path / "LOC_synset_mapping.txt"
    mapping_file.write_text("\n".join(synset_lines) + "\n")

    # Directory structure
    imageset_dir = tmp_path / "ILSVRC" / "ImageSets" / "CLS-LOC"
    imageset_dir.mkdir(parents=True, exist_ok=True)

    train_data_dir = tmp_path / "ILSVRC" / "Data" / "CLS-LOC" / "train"
    train_data_dir.mkdir(parents=True, exist_ok=True)

    val_data_dir = tmp_path / "ILSVRC" / "Data" / "CLS-LOC" / "val"
    val_data_dir.mkdir(parents=True, exist_ok=True)

    # Build train_cls.txt annotations and (optionally) JPEG files
    annotation_lines = []
    for wnid in annotation_wnids:
        wnid_dir = train_data_dir / wnid
        if create_jpegs:
            wnid_dir.mkdir(parents=True, exist_ok=True)
        for i in range(5):
            image_name = f"{wnid}/{wnid}_{i:04d}"
            annotation_lines.append(f"{image_name} {i}")
            if create_jpegs:
                (wnid_dir / f"{wnid}_{i:04d}.JPEG").write_bytes(b"\xff\xd8dummy")

    train_cls = imageset_dir / "train_cls.txt"
    train_cls.write_text("\n".join(annotation_lines) + "\n")

    # Build val.txt annotations, LOC_val_solution.csv, and val JPEG files
    val_annotation_lines = []
    val_solution_lines = ["ImageId,PredictionString"]
    val_img_counter = 1
    for wnid in annotation_wnids:
        for i in range(5):
            image_id = f"ILSVRC2012_val_{val_img_counter:08d}"
            val_annotation_lines.append(f"{image_id} {val_img_counter}")
            val_solution_lines.append(f"{image_id},{wnid} 0 0 100 100")
            if create_jpegs:
                (val_data_dir / f"{image_id}.JPEG").write_bytes(b"\xff\xd8dummy")
            val_img_counter += 1

    val_txt = imageset_dir / "val.txt"
    val_txt.write_text("\n".join(val_annotation_lines) + "\n")

    val_solution = tmp_path / "LOC_val_solution.csv"
    val_solution.write_text("\n".join(val_solution_lines) + "\n")

    return tmp_path


@pytest.fixture
def mock_imagenet(tmp_path):
    """Full mock ImageNet with synset mapping, annotations, and JPEG files."""
    return _build_mock_imagenet(tmp_path)


@pytest.fixture
def mock_imagenet_no_files(tmp_path):
    """Mock ImageNet with mapping and annotations but NO JPEG files on disk."""
    return _build_mock_imagenet(tmp_path, create_jpegs=False)


@pytest.fixture
def mock_imagenet_empty(tmp_path):
    """Mock ImageNet with empty train_cls.txt and val.txt (no annotations)."""
    base = tmp_path

    mapping_file = base / "LOC_synset_mapping.txt"
    mapping_file.write_text("\n".join(MOCK_SYNSET_LINES) + "\n")

    imageset_dir = base / "ILSVRC" / "ImageSets" / "CLS-LOC"
    imageset_dir.mkdir(parents=True, exist_ok=True)
    (imageset_dir / "train_cls.txt").write_text("")
    (imageset_dir / "val.txt").write_text("")

    train_data_dir = base / "ILSVRC" / "Data" / "CLS-LOC" / "train"
    train_data_dir.mkdir(parents=True, exist_ok=True)

    val_data_dir = base / "ILSVRC" / "Data" / "CLS-LOC" / "val"
    val_data_dir.mkdir(parents=True, exist_ok=True)

    # LOC_val_solution.csv with header only
    (base / "LOC_val_solution.csv").write_text("ImageId,PredictionString\n")

    return base
