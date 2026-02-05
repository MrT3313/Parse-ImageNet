from pathlib import Path
from collections import defaultdict
import random
import argparse

# keywords
from keywords.birds import bird_keywords

def get_image_paths_by_keywords(base_path, keywords, num_images=200):
    """
    Extract file paths for images matching specified keywords.
    
    Args:
        base_path: Path to ImageNet-Subset directory
        keywords: List of keywords to match in category names
        num_images: Number of random images to extract (default: 200)
    
    Returns:
        List of Path objects to the selected images
    """
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
    print(f"SEARCHING WITH KEYWORDS: {keywords}")
    print("=" * 80)
    
    matching_wnids = []
    for wnid, category_name in synset_mapping.items():
        if any(keyword.lower() in category_name.lower() for keyword in keywords):
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
    parser.add_argument('--keywords', nargs='+', default=bird_keywords, 
                        help='Keywords to match in category names (default: bird)')
    parser.add_argument('--base_path', type=str, 
                        default='/Users/mrt/Documents/MrT/code/computer-vision/image-bank/ImageNet-Subset',
                        help='Path to ImageNet-Subset directory')
    
    args = parser.parse_args()
    
    base_path = Path(args.base_path)
    
    # Extract image paths
    image_paths = get_image_paths_by_keywords(base_path, args.keywords, num_images=args.num_images)
    
    # Print first 10 paths as example
    if image_paths:
        print("\nFirst 10 image paths:")
        for i, path in enumerate(image_paths[:10], 1):
            print(f"{i}. {path}")

if __name__ == "__main__":
    main()