from pathlib import Path
from collections import defaultdict
import random

def extract_category_paths(base_path, keywords, num_images=200):
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
    print(f"CATEGORIES MATCHING KEYWORDS: {keywords}")
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


# Example usage
if __name__ == "__main__":
    base_path = Path("/Users/mrt/Documents/MrT/code/computer-vision/image-bank/ImageNet-Subset")
    
    # Define your keywords
    bird_keywords = [
        'bird', 'finch', 'robin', 'eagle', 'hawk', 'owl', 'sparrow', 
        'warbler', 'hummingbird', 'jay', 'cardinal', 'chickadee',
        'duck', 'goose', 'swan', 'crane', 'heron', 'pelican',
        'parrot', 'cockatoo', 'macaw', 'penguin', 'ostrich',
        'brambling', 'bunting', 'junco', 'oriole', 'magpie',
        'cock', 'hen', 'rooster', 'chicken', 'grouse', 'partridge',
        'quail', 'pheasant', 'peacock', 'flamingo', 'stork',
        'albatross', 'cormorant', 'kingfisher', 'hornbill',
        'toucan', 'woodpecker', 'flycatcher', 'shrike', 'vireo',
        'wren', 'thrush', 'mockingbird', 'starling', 'pipit'
    ]
    
    # Extract 200 bird image paths
    image_paths = extract_category_paths(base_path, bird_keywords, num_images=200)
    
    # Print first 10 paths as example
    print("First 10 image paths:")
    for i, path in enumerate(image_paths[:10], 1):
        print(f"{i}. {path}")
    
    # Save paths to a text file
    output_file = base_path / "bird_image_paths.txt"
    with open(output_file, 'w') as f:
        for path in image_paths:
            f.write(f"{path}\n")
    
    print(f"\nAll paths saved to: {output_file}")

# from pathlib import Path
# from collections import defaultdict
# import random
# import shutil

# # Define paths
# base_path = Path("/Users/mrt/Documents/MrT/code/computer-vision/image-bank/ImageNet-Subset")
# train_annotations = base_path / "ILSVRC" / "ImageSets" / "CLS-LOC" / "train_cls.txt"
# synset_mapping_file = base_path / "LOC_synset_mapping.txt"
# data_path = base_path / "ILSVRC" / "Data" / "CLS-LOC" / "train"

# # Load synset mapping (wnid -> category names)
# print("Loading category names...")
# synset_mapping = {}
# with open(synset_mapping_file, 'r') as f:
#     for line in f:
#         parts = line.strip().split(maxsplit=1)
#         if len(parts) == 2:
#             wnid = parts[0]
#             category_name = parts[1]
#             synset_mapping[wnid] = category_name

# print(f"Loaded {len(synset_mapping)} categories\n")

# # Parse training annotations
# print("Parsing training annotations...")
# category_images = defaultdict(list)

# with open(train_annotations, 'r') as f:
#     for line in f:
#         parts = line.strip().split()
#         if len(parts) >= 1:
#             image_path = parts[0]  # e.g., "n01440764/n01440764_10026"
#             wnid = image_path.split('/')[0]  # Extract the wnid
#             category_images[wnid].append(image_path)

# print(f"Found {len(category_images)} unique categories\n")

# # Display categories with names
# print("=" * 80)
# print("ALL CATEGORIES:")
# print("=" * 80)
# for wnid in sorted(category_images.keys()):
#     category_name = synset_mapping.get(wnid, "Unknown")
#     count = len(category_images[wnid])
#     print(f"{wnid}: {category_name} ({count} images)")

# # Find bird categories
# print("\n" + "=" * 80)
# print("BIRD CATEGORIES:")
# print("=" * 80)
# bird_keywords = ['bird', 'finch', 'robin', 'eagle', 'hawk', 'owl', 'sparrow', 
#                  'warbler', 'hummingbird', 'jay', 'cardinal', 'chickadee',
#                  'duck', 'goose', 'swan', 'crane', 'heron', 'pelican',
#                  'parrot', 'cockatoo', 'macaw', 'penguin', 'ostrich',
#                  'brambling', 'bunting', 'junco', 'oriole', 'magpie']

# bird_wnids = []
# for wnid, category_name in synset_mapping.items():
#     if any(keyword in category_name.lower() for keyword in bird_keywords):
#         if wnid in category_images:
#             bird_wnids.append(wnid)
#             count = len(category_images[wnid])
#             print(f"{wnid}: {category_name} ({count} images)")

# print(f"\nTotal bird categories found: {len(bird_wnids)}")

# # Collect all bird images
# all_bird_images = []
# for wnid in bird_wnids:
#     all_bird_images.extend(category_images[wnid])

# print(f"Total bird images available: {len(all_bird_images)}")

# # Extract 200 random bird images
# if len(all_bird_images) > 0:
#     num_to_extract = min(200, len(all_bird_images))
#     selected_images = random.sample(all_bird_images, num_to_extract)
    
#     output_dir = base_path / "bird_subset"
#     output_dir.mkdir(exist_ok=True)
    
#     print(f"\nExtracting {num_to_extract} bird images to {output_dir}...")
    
#     copied = 0
#     for img_path in selected_images:
#         # img_path is like "n01440764/n01440764_10026"
#         src = data_path / f"{img_path}.JPEG"
        
#         if src.exists():
#             dst = output_dir / f"{img_path.replace('/', '_')}.JPEG"
#             shutil.copy(src, dst)
#             copied += 1
#             if copied % 50 == 0:
#                 print(f"Copied {copied} images...")
    
#     print(f"\nDone! Copied {copied} bird images to {output_dir}")
# else:
#     print("\nNo bird images found!")

# # from pathlib import Path
# # from collections import defaultdict

# # from pathlib import Path
# # from collections import defaultdict

# # # Define paths
# # base_path = Path("/Users/mrt/Documents/MrT/code/computer-vision/image-bank/ImageNet-Subset")
# # annotations_path = base_path / "ILSVRC" / "Annotations" / "CLS-LOC"
# # data_path = base_path / "ILSVRC" / "Data" / "CLS-LOC"

# # # Read the training annotations
# # train_annotations = base_path / "ILSVRC" / "ImageSets" / "CLS-LOC" / "train_cls.txt"

# # print(f"Reading annotations from: {train_annotations}")
# # print("Parsing file (this may take a moment for large files)...")

# # # Dictionary to store image paths by category
# # category_images = defaultdict(list)

# # # Parse annotations
# # line_count = 0
# # with open(train_annotations, 'r') as f:
# #     for line in f:
# #         parts = line.strip().split()
# #         if len(parts) >= 2:
# #             image_name = parts[0]
# #             wnid = parts[1]
# #             category_images[wnid].append(image_name)
# #             line_count += 1
            
# #             if line_count % 10000 == 0:
# #                 print(f"Processed {line_count} images...")

# # print(f"\nDone! Processed {line_count} total images")
# # print(f"Total categories: {len(category_images)}")
# # print("\nFirst 10 categories:")
# # for wnid in sorted(category_images.keys())[:10]:
# #     print(f"{wnid}: {len(category_images[wnid])} images")