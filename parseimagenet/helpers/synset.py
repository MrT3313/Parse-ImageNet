from pathlib import Path

def get_synset_mapping(base_path):
    """Read LOC_synset_mapping.txt and return a WNID-to-category-name mapping.

    Args:
        base_path: Path to ImageNet-Subset directory (str or Path).

    Returns:
        dict[str, str] mapping each WNID to its full category string.
    """
    synset_mapping_file = Path(base_path) / "LOC_synset_mapping.txt"
    synset_mapping = {}
    with open(synset_mapping_file, 'r') as f:
        for line in f:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                synset_mapping[parts[0]] = parts[1]
    return synset_mapping
