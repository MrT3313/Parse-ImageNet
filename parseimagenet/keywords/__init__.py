from .bird_breeds import bird_breeds
from .dog_breeds import dog_breeds, wild_canid_breeds
from .snake_breeds import snake_breeds

KEYWORD_PRESETS = {
    "birds": bird_breeds,
    "dogs": dog_breeds,
    "wild_canids": wild_canid_breeds,
    "snakes": snake_breeds,
}


def get_available_presets():
    """Return list of available preset names."""
    return list(KEYWORD_PRESETS.keys())


__all__ = ['bird_breeds', 'dog_breeds', 'wild_canid_breeds', 'snake_breeds']
