from collections import defaultdict


def parse_train_annotations(annotations_file):
    """Parse train_cls.txt and group image stems by WNID.

    Args:
        annotations_file: Path to train_cls.txt.

    Returns:
        defaultdict[str, list[str]] mapping WNID to image path stems.
    """
    category_images = defaultdict(list)
    with open(annotations_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 1:
                image_path = parts[0]
                wnid = image_path.split('/')[0]
                category_images[wnid].append(image_path)
    return category_images


def parse_val_annotations(annotations_file, base_path):
    """Parse val.txt + LOC_val_solution.csv and group image stems by WNID.

    Args:
        annotations_file: Path to val.txt.
        base_path: Path to ImageNet-Subset directory (to locate LOC_val_solution.csv).

    Returns:
        defaultdict[str, list[str]] mapping WNID to image ID stems.
    """
    val_solution_file = base_path / "LOC_val_solution.csv"
    image_to_wnid = {}
    with open(val_solution_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("ImageId"):
                continue
            parts = line.split(",")
            if len(parts) >= 2:
                image_id = parts[0]
                wnid = parts[1].split()[0]
                image_to_wnid[image_id] = wnid

    category_images = defaultdict(list)
    with open(annotations_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 1:
                image_id = parts[0]
                if image_id in image_to_wnid:
                    wnid = image_to_wnid[image_id]
                    category_images[wnid].append(image_id)
    return category_images


def parse_annotations(annotations_file, base_path, source):
    """Dispatch to the appropriate annotation parser based on source.

    Args:
        annotations_file: Path to the annotation file.
        base_path: Path to ImageNet-Subset directory.
        source: "train" or "val".

    Returns:
        defaultdict[str, list[str]] mapping WNID to image stems.
    """
    if source == "train":
        return parse_train_annotations(annotations_file)
    else:
        return parse_val_annotations(annotations_file, base_path)
