# ParseImageNet

Extract image file paths from ImageNet by matching category keywords. Useful for creating custom subsets of ImageNet for training or evaluation.

[![PyPI Version](https://img.shields.io/pypi/v/parseimagenet)](https://pypi.org/project/parseimagenet/)
[![Python Version](https://img.shields.io/pypi/pyversions/parseimagenet)](https://pypi.org/project/parseimagenet/)
[![License](https://img.shields.io/github/license/MrT3313/Parse-ImageNet)](https://github.com/MrT3313/Parse-ImageNet/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/parseimagenet)](https://pypi.org/project/parseimagenet/)

## [Kaggle Dataset](https://www.kaggle.com/competitions/imagenet-object-localization-challenge/data)

## Prerequisites

- Python 3.8+
- ImageNet dataset (or a subset) with the standard ILSVRC directory structure:
  ```
  ImageNet-Subset/
  ├── LOC_synset_mapping.txt
  └── ILSVRC/
      ├── ImageSets/
      │   └── CLS-LOC/
      │       └── train_cls.txt
      └── Data/
          └── CLS-LOC/
              └── train/
                  ├── n01440764/
                  │   ├── n01440764_10026.JPEG
                  │   └── ...
                  └── ...
  ```

## Installation

```bash
pip install parseimagenet
```

For local development:

```bash
git clone https://github.com/MrT3313/Parse-ImageNet.git
pip install -e ./Parse-ImageNet
```

## Usage

> [!NOTE]
> 
> [Example Notebook](/DOCS/ExampleNotebook.ipynb)

### In Jupyter Lab / Jupyter Notebook

```python
from pathlib import Path
from parseimagenet import get_image_paths_by_keywords

# Set the path to your ImageNet directory
base_path = Path('/path/to/your/ImageNet-Subset')
# ex: /Users/mrt/Documents/MrT/code/computer-vision/image-bank/ImageNet-Subset

# Use the default "birds" preset
image_paths = get_image_paths_by_keywords(base_path=base_path)

# image_paths is a list of Path objects
print(f"Found {len(image_paths)} images")
print(image_paths[:5])
```

#### Using Preset Keywords

Presets are predefined keyword lists for common categories:

```python
from parseimagenet import get_image_paths_by_keywords # main function
from parseimagenet import get_available_presets, KEYWORD_PRESETS # helpers

# See available presets
print(get_available_presets())  # ['birds']

# Use a specific preset
image_paths = get_image_paths_by_keywords(
    base_path=base_path,
    preset="birds",
    num_images=200
)

# Access preset keywords directly
print(KEYWORD_PRESETS["birds"])
```

#### Using Custom Keywords

Custom keywords override the preset:

```python
image_paths = get_image_paths_by_keywords(
    base_path=base_path,
    keywords=['dog', 'puppy', 'hound'],
    num_images=100
)
```

> [!NOTE]
> 
> you can find all applicable categories in the `LOC_synset_mapping.txt` file

### Command Line

```bash
# Use default preset (birds)
python -m parseimagenet.ParseImageNetSubset --base_path /path/to/ImageNet-Subset

# Use a specific preset
python -m parseimagenet.ParseImageNetSubset --base_path /path/to/ImageNet-Subset --preset birds --num_images 100

# Use custom keywords (overrides preset)
python -m parseimagenet.ParseImageNetSubset --base_path /path/to/ImageNet-Subset --keywords dog puppy --num_images 100
```
