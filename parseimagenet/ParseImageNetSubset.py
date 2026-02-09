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

def get_image_paths_by_keywords(base_path, preset="birds", keywords=None, num_images=200):
    """
    Extract file paths for images matching specified keywords.

    Args:
        base_path: Path to ImageNet-Subset directory
        preset: Name of predefined keyword list (default: "birds").
                Available presets: "birds". Use get_available_presets() to see all.
        keywords: Custom list of keywords. If provided, overrides preset.
        num_images: Number of random images to extract (default: 200)

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

    train_annotations = base_path / "ILSVRC" / "ImageSets" / "CLS-LOC" / "train_cls.txt"
    synset_mapping_file = base_path / "LOC_synset_mapping.txt"
    data_path = base_path / "ILSVRC" / "Data" / "CLS-LOC" / "train"
    
    # Load synset mapping (wnid -> category names)
    print("")
    print("Loading category names...")
    synset_mapping = {}
    with open(synset_mapping_file, 'r') as f:
        for line in f:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                wnid = parts[0]
                category_name = parts[1]
                synset_mapping[wnid] = category_name
    
    print(f"Loaded {len(synset_mapping)} categories\n")
    
    # Parse training annotations
    print("Parsing training annotations...")
    category_images = defaultdict(list)
    
    with open(train_annotations, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 1:
                image_path = parts[0]  # e.g., "n01440764/n01440764_10026"
                wnid = image_path.split('/')[0]  # Extract the wnid
                category_images[wnid].append(image_path)
    
    print(f"Found {len(category_images)} unique categories\n")
    
    # Find matching categories
    print("=" * 80)
    print(f"SEARCHING WITH KEYWORDS: {search_keywords}")
    print("=" * 80)

    matching_wnids = []
    for wnid, category_name in synset_mapping.items():
        if any(re.search(rf'\b{re.escape(keyword)}\b', category_name, re.IGNORECASE) for keyword in search_keywords):
            if wnid in category_images:
                matching_wnids.append(wnid)
                count = len(category_images[wnid])
                print(f"{wnid}: {category_name} ({count} images)")
    
    print(f"\n{'=' * 80}")
    print(f"Total matching categories: {len(matching_wnids)}")
    print(f"{'=' * 80}\n")
    
    # Collect all matching images
    all_matching_images = []
    for wnid in matching_wnids:
        all_matching_images.extend(category_images[wnid])
    
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
        
        print(f"\nSelected {num_to_select} random images")
        
        # Verify how many actually exist
        existing = sum(1 for p in full_paths if p.exists())
        print(f"Verified {existing}/{num_to_select} files exist on disk\n")
        
        return full_paths
    else:
        print("\nNo matching images found!")
        return []


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract ImageNet image paths by category keywords')
    parser.add_argument('--num_images', type=int, default=200,
                        help='Number of random images to extract (default: 200)')
    parser.add_argument('--preset', type=str, default='birds',
                        help=f'Predefined keyword preset (default: birds). Available: {get_available_presets()}')
    parser.add_argument('--keywords', nargs='+', default=None,
                        help='Custom keywords to match in category names (overrides --preset)')
    parser.add_argument('--base_path', type=str,
                        default='/Users/mrt/Documents/MrT/code/computer-vision/image-bank/ImageNet-Subset',
                        help='Path to ImageNet-Subset directory')

    args = parser.parse_args()

    base_path = Path(args.base_path)

    # Extract image paths
    image_paths = get_image_paths_by_keywords(
        base_path,
        preset=args.preset,
        keywords=args.keywords,
        num_images=args.num_images
    )
    
    # Print first 10 paths as example
    if image_paths:
        print("\nFirst 10 image paths:")
        for i, path in enumerate(image_paths[:10], 1):
            print(f"{i}. {path}")

if __name__ == "__main__":
    main()