from pathlib import Path
from collections import defaultdict
import random
import argparse
import re

from .keywords import bird_breeds, dog_breeds, wild_canid_breeds, snake_breeds

# Registry of predefined keyword presets
KEYWORD_PRESETS = {
    "birds": bird_breeds,
    "dogs": dog_breeds,
    "wild_canids": wild_canid_breeds,
    "snakes": snake_breeds,
}

def get_available_presets():
    """Return list of available preset names."""
    return list(KEYWORD_PRESETS.keys())

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

def get_image_paths_by_keywords(base_path, preset="birds", keywords=None, num_images=200, source="train", silent=True):
    """
    Extract file paths for images matching specified keywords.

    Args:
        base_path: Path to ImageNet-Subset directory
        preset: Name of predefined keyword list (default: "birds").
                Available presets: "birds". Use get_available_presets() to see all.
        keywords: Custom list of keywords. If provided, overrides preset.
        num_images: Number of random images to extract (default: 200)
        source: Which data split to use, "train" or "val" (default: "train")
        silent: If True, suppress all print output (default: True)

    Returns:
        List of Path objects to the selected images
    """
    # Determine which keywords to use
    if keywords is not None:
        # Custom keywords provided - validate it's a list
        if isinstance(keywords, str):
            raise TypeError("keywords must be a list of strings, not a single string. Use keywords=['your_keyword'] instead.")
        if not isinstance(keywords, list):
            raise TypeError("keywords must be a list of strings.")
        search_keywords = keywords
    else:
        # Use preset
        if preset not in KEYWORD_PRESETS:
            available = get_available_presets()
            raise ValueError(f"Unknown preset '{preset}'. Available presets: {available}")
        search_keywords = KEYWORD_PRESETS[preset]

    valid_sources = ("train", "val")
    if source not in valid_sources:
        raise ValueError(f"Unknown source '{source}'. Must be one of: {list(valid_sources)}")

    if source == "train":
        annotations_file = base_path / "ILSVRC" / "ImageSets" / "CLS-LOC" / "train_cls.txt"
        data_path = base_path / "ILSVRC" / "Data" / "CLS-LOC" / "train"
    else:
        annotations_file = base_path / "ILSVRC" / "ImageSets" / "CLS-LOC" / "val.txt"
        data_path = base_path / "ILSVRC" / "Data" / "CLS-LOC" / "val"

    # Load synset mapping (wnid -> category names)
    if not silent:
        print("")
        print("Loading category names...")
    synset_mapping = get_synset_mapping(base_path)

    if not silent:
        print(f"Loaded {len(synset_mapping)} categories\n")

    # Parse annotations
    if not silent:
        print(f"Parsing {source} annotations...")
    category_images = defaultdict(list)

    if source == "train":
        with open(annotations_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 1:
                    image_path = parts[0]  # e.g., "n01440764/n01440764_10026"
                    wnid = image_path.split('/')[0]  # Extract the wnid
                    category_images[wnid].append(image_path)
    else:
        # Val: build image_id -> wnid mapping from LOC_val_solution.csv
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

        # Read val.txt and group images by wnid
        with open(annotations_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 1:
                    image_id = parts[0]  # e.g., "ILSVRC2012_val_00000001"
                    if image_id in image_to_wnid:
                        wnid = image_to_wnid[image_id]
                        category_images[wnid].append(image_id)
    
    if not silent:
        print(f"Found {len(category_images)} unique categories\n")

    # Find matching categories
    if not silent:
        print("=" * 80)
        print(f"SEARCHING WITH KEYWORDS: {search_keywords}")
        print("=" * 80)

    matching_wnids = []
    for wnid, category_name in synset_mapping.items():
        if any(re.search(rf'\b{re.escape(keyword)}\b', category_name, re.IGNORECASE) for keyword in search_keywords):
            if wnid in category_images:
                matching_wnids.append(wnid)
                if not silent:
                    count = len(category_images[wnid])
                    print(f"{wnid}: {category_name} ({count} images)")
    
    if not silent:
        print(f"\n{'=' * 80}")
        print(f"Total matching categories: {len(matching_wnids)}")
        print(f"{'=' * 80}\n")
    
    # Collect all matching images
    all_matching_images = []
    for wnid in matching_wnids:
        all_matching_images.extend(category_images[wnid])
    
    if not silent:
        print(f"Total matching images available: {len(all_matching_images)}")
    
    # Select random images
    if len(all_matching_images) > 0:
        num_to_select = min(num_images, len(all_matching_images))
        selected_image_paths = random.sample(all_matching_images, num_to_select)
        
        # Convert to full file paths
        full_paths = []
        for img_path in selected_image_paths:
            full_path = data_path / f"{img_path}.JPEG"
            full_paths.append(full_path)
        
        if not silent:
            print(f"\nSelected {num_to_select} random images")

        # Verify how many actually exist
        existing = sum(1 for p in full_paths if p.exists())
        if not silent:
            print(f"Verified {existing}/{num_to_select} files exist on disk\n")
        
        return full_paths
    else:
        if not silent:
            print("\nNo matching images found!")
        return []


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract ImageNet image paths by category keywords')
    parser.add_argument('--num_images', type=int, default=200,
                        help='Number of random images to extract (default: 200)')
    parser.add_argument('--preset', type=str, default='birds',
                        help=f'Predefined keyword preset (default: birds). Available: {get_available_presets()}')
    parser.add_argument('--keywords', type=str, default=None,
                        help='Comma-separated keywords to match in category names (overrides --preset)')
    parser.add_argument('--source', type=str, default='train',
                        choices=['train', 'val'],
                        help='Data split to use: train or val (default: train)')
    parser.add_argument('--base_path', type=str,
                        default='/Users/mrt/Documents/MrT/code/computer-vision/image-bank/ImageNet-Subset',
                        help='Path to ImageNet-Subset directory')

    args = parser.parse_args()

    base_path = Path(args.base_path)

    # Extract image paths
    image_paths = get_image_paths_by_keywords(
        base_path,
        preset=args.preset,
        keywords=[k.strip() for k in args.keywords.split(',')] if args.keywords else None,
        num_images=args.num_images,
        source=args.source,
        silent=False,
    )
    
    # Print first 10 paths as example
    if image_paths:
        print("\nFirst 10 image paths:")
        for i, path in enumerate(image_paths[:10], 1):
            print(f"{i}. {path}")

if __name__ == "__main__":
    main()