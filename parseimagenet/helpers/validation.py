def validate_params(preset, keywords, keyword_presets, source):
    """Validate source and resolve search keywords.

    Args:
        preset: Name of predefined keyword list, or None.
        keywords: Custom list of keywords, or None.
        keyword_presets: Dict mapping preset names to keyword lists.
        source: "train" or "val".

    Returns:
        list[str] of keywords, or None for all-categories mode.

    Raises:
        ValueError: If source or preset is invalid.
        TypeError: If keywords is not a list.
    """
    _validate_source(source)
    return _resolve_search_keywords(preset, keywords, keyword_presets)

def _validate_source(source):
    """Validate that source is 'train' or 'val'.

    Raises:
        ValueError: If source is not a valid split name.
    """
    valid_sources = ("train", "val")
    if source not in valid_sources:
        raise ValueError(f"Unknown source '{source}'. Must be one of: {list(valid_sources)}")

def _resolve_search_keywords(preset, keywords, keyword_presets):
    """Determine which keywords to use for filtering.

    Args:
        preset: Name of predefined keyword list, or None.
        keywords: Custom list of keywords, or None.
        keyword_presets: Dict mapping preset names to keyword lists.

    Returns:
        list[str] of keywords, or None for all-categories mode.

    Raises:
        TypeError: If keywords is not a list.
        ValueError: If preset name is not recognized.
    """
    if keywords is not None:
        if isinstance(keywords, str):
            raise TypeError("keywords must be a list of strings, not a single string. Use keywords=['your_keyword'] instead.")
        if not isinstance(keywords, list):
            raise TypeError("keywords must be a list of strings.")
        return keywords
    elif preset is not None:
        if preset not in keyword_presets:
            available = list(keyword_presets.keys())
            raise ValueError(f"Unknown preset '{preset}'. Available presets: {available}")
        return keyword_presets[preset]
    else:
        return None



