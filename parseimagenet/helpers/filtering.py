import re


def filter_categories(synset_mapping, category_images, search_keywords):
    """Return WNIDs that match the given keywords (or all WNIDs if keywords is None).

    Args:
        synset_mapping: Dict mapping WNID to category name string.
        category_images: Dict mapping WNID to list of image stems.
        search_keywords: List of keyword strings, or None for all categories.

    Returns:
        List of matching WNID strings.
    """
    if search_keywords is None:
        return list(category_images.keys())

    matching_wnids = []
    for wnid, category_name in synset_mapping.items():
        if any(re.search(rf'\b{re.escape(keyword)}\b', category_name, re.IGNORECASE) for keyword in search_keywords):
            if wnid in category_images:
                matching_wnids.append(wnid)
    return matching_wnids
