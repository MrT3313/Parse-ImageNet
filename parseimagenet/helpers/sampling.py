import random


def collect_and_sample(category_images, matching_wnids, num_images, data_path):
    """Gather all images for matching WNIDs, sample a subset, and resolve full paths.

    Args:
        category_images: Dict mapping WNID to list of image stems.
        matching_wnids: List of WNIDs to collect images from.
        num_images: Maximum number of images to sample.
        data_path: Base data directory Path.

    Returns:
        Tuple of (full_paths, all_count) where full_paths is a list of Path objects
        and all_count is the total number of matching images available.
    """
    all_matching_images = []
    for wnid in matching_wnids:
        all_matching_images.extend(category_images[wnid])

    if len(all_matching_images) > 0:
        num_to_select = min(num_images, len(all_matching_images))
        selected = random.sample(all_matching_images, num_to_select)
    else:
        selected = []

    # Resolve stems to full paths
    full_paths = []
    for stem in selected:
        stem_path = data_path / stem
        matches = list(stem_path.parent.glob(f"{stem_path.name}.*"))
        if matches:
            full_paths.append(matches[0])
        else:
            full_paths.append(stem_path)

    return full_paths, len(all_matching_images)


def count_existing(paths):
    """Return count of paths that exist on disk.

    Args:
        paths: Iterable of Path objects.

    Returns:
        int count of existing files.
    """
    return sum(1 for p in paths if p.exists())
