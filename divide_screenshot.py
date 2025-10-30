"""Image slicing helpers for Marvel Snap board captures."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from PIL import Image


@dataclass(frozen=True)
class Region:
    """Screen-space fractional bounds describing a crop target."""

    left: float
    top: float
    right: float
    bottom: float

    def to_pixels(self, width: int, height: int) -> tuple[int, int, int, int]:
        """Convert fractional bounds into pixel coordinates."""
        return (
            int(width * self.left),
            int(height * self.top),
            int(width * self.right),
            int(height * self.bottom),
        )


REGIONS: dict[str, Region] = {
    "your_cards": Region(0.0, 0.75, 1.0, 0.890),
    "location1": Region(0.160, 0.215, 0.385, 0.760),
    "location2": Region(0.385, 0.215, 0.610, 0.760),
    "location3": Region(0.610, 0.215, 0.835, 0.760),
    "energy_turns": Region(0.420, 0.895, 1.0, 1.0),
}


def divide_screenshot(image_path: Path | str, output_dir: Path | str | None = None) -> Dict[str, Path]:
    """
    Slice the full-board screenshot into focused regions.

    Parameters
    ----------
    image_path:
        Path to the captured screenshot.
    output_dir:
        Optional directory to write the cropped images. Defaults to the screenshot's
        parent directory.

    Returns
    -------
    Dict[str, Path]
        Mapping of region names to the saved image paths.
    """
    image_path = Path(image_path)
    if output_dir is None:
        output_dir = image_path.parent
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(image_path) as image:
        width, height = image.size
        saved_paths: Dict[str, Path] = {}

        for name, region in REGIONS.items():
            crop_box = region.to_pixels(width, height)
            cropped = image.crop(crop_box)
            save_path = output_dir / f"{name}.png"
            cropped.save(save_path)
            saved_paths[name] = save_path

    return saved_paths


if __name__ == "__main__":
    divide_screenshot("screenshot.png")
