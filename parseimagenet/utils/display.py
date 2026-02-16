def print_filter_results(search_keywords, matching_wnids, synset_mapping, category_images):
    """Print category match results (verbose mode only)."""
    if search_keywords is None:
        print("SELECTING FROM ALL CATEGORIES (no keyword filter)\n")
        for wnid in matching_wnids:
            category_name = synset_mapping.get(wnid, "unknown")
            count = len(category_images[wnid])
            print(f"{wnid}: {category_name} ({count} images)")
        print(f"\n{'=' * 80}")
        print(f"Total categories: {len(matching_wnids)}")
        print(f"{'=' * 80}\n")
    else:
        print(f"SEARCHING WITH KEYWORDS:\n{search_keywords}\n")
        for wnid in matching_wnids:
            category_name = synset_mapping.get(wnid, "unknown")
            count = len(category_images[wnid])
            print(f"{wnid}: {category_name} ({count} images)")
        print(f"\n{'=' * 80}")
        print(f"Total matching categories: {len(matching_wnids)}")
        print(f"{'=' * 80}\n")
