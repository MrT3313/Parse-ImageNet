from pathlib import Path
import argparse

from .keywords import KEYWORD_PRESETS, get_available_presets
from .helpers.validation import validate_params
from .helpers.paths import resolve_paths
from .helpers.annotations import parse_annotations
from .helpers.filtering import filter_categories
from .helpers.sampling import collect_and_sample, count_existing
from .helpers.synset import get_synset_mapping
from .utils import print_filter_results

def get_image_paths_by_keywords(base_path, preset=None, keywords=None, num_images=200, source="train", silent=True):
    """
    Extract file paths for images matching specified keywords.

    Args:
        base_path: Path to ImageNet-Subset directory
        preset: Name of predefined keyword list (default: None).
                Available presets: use get_available_presets() to see all.
                When None (with keywords=None), returns random images from all categories.
        keywords: Custom list of keywords. If provided, overrides preset.
        num_images: Number of random images to extract (default: 200)
        source: Which data split to use, "train" or "val" (default: "train")
        silent: If True, suppress all print output (default: True)

    Returns:
        List of Path objects to the selected images
    """
    # VALIDATE PARAMS: keywords, preset, source
    search_keywords = validate_params(preset, keywords, KEYWORD_PRESETS, source)

    # RESOLVE PATHS: annotations_file, data_path
    annotations_file, data_path = resolve_paths(base_path, source)

    # GET SYNSET MAPPING: wnid -> category names
    synset_mapping = get_synset_mapping(base_path)
    if not silent:
        print(f"Loaded {len(synset_mapping)} possible categories\n")

    # PARSE ANNOTATIONS: category_images
    category_images = parse_annotations(annotations_file, base_path, source)
    if not silent:
        print(f"Found {len(category_images)} unique categories\n")

    # FILTER CATEGORIES: matching_wnids
    matching_wnids = filter_categories(synset_mapping, category_images, search_keywords)
    if not silent:
        print_filter_results(search_keywords, matching_wnids, synset_mapping, category_images)

    # COLLECT AND SAMPLE IMAGES: selected_paths, total_available
    selected_paths, total_available = collect_and_sample(category_images, matching_wnids, num_images, data_path)
    if not silent:
        print(f"Total matching images available: {total_available}")

    # COUNT EXISTING FILES: existing
    if selected_paths:
        if not silent:
            existing = count_existing(selected_paths)
            print(f"\nSelected {len(selected_paths)} images")
            print(f"Verified {existing}/{len(selected_paths)} files exist on disk\n")
        return selected_paths
    else:
        if not silent:
            print("\nNo matching images found!\n")
        return []


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract ImageNet image paths by category keywords')
    parser.add_argument('--num_images', type=int, default=200,
                        help='Number of images to extract (default: 200)')
    parser.add_argument('--preset', type=str, default='birds',
                        help=f'Predefined keyword preset (default: birds). Available: {get_available_presets()}. Use "none" for all categories.')
    parser.add_argument('--keywords', type=str, default=None,
                        help='Comma-separated keywords to match in category names (overrides --preset)')
    parser.add_argument('--source', type=str, default='train',
                        choices=['train', 'val'],
                        help='Data split to use: train or val (default: train)')
    parser.add_argument('--base_path', type=str,
                        default='/Users/mrt/Documents/MrT/code/computer-vision/image-bank/ImageNet-Subset',
                        help='Path to ImageNet-Subset directory')

    args = parser.parse_args()

    # Convert "none" string to Python None for all-categories mode
    if args.preset and args.preset.lower() == "none":
        args.preset = None

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
