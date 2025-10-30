"""Card metadata loading helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Dict


def load_card_abilities(file_path: Path | str) -> Dict[str, str]:
    """
    Load card ability descriptions from a ``card_abilities.txt`` file.

    Parameters
    ----------
    file_path:
        Path to the ability file. Each line must follow ``Card Name: ability text``.

    Returns
    -------
    Dict[str, str]
        Mapping of card names to their ability descriptions.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    card_abilities: Dict[str, str] = {}
    with file_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():  # Skip empty lines
                card_name, ability = line.split(":", 1)
                card_abilities[card_name.strip()] = ability.strip()

    return card_abilities


if __name__ == "__main__":
    abilities = load_card_abilities("card_abilities.txt")
    for card, ability in abilities.items():
        print(f"{card}: {ability}")
