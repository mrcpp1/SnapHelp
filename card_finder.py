"""Utilities for reconciling card references with ability metadata."""

from __future__ import annotations

from pathlib import Path
from typing import Set

from read_card_abilities import load_card_abilities


def load_card_names(file_path: Path | str) -> Set[str]:
    """Load distinct card names from a newline-delimited text file."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with file_path.open("r", encoding="utf-8") as handle:
        return {line.strip() for line in handle if line.strip()}


def find_missing_cards(all_cards_path: Path | str, abilities_path: Path | str) -> Set[str]:
    """Return the set of cards that have no entry in ``card_abilities``."""
    all_cards = load_card_names(all_cards_path)
    ability_cards = set(load_card_abilities(abilities_path).keys())
    return all_cards - ability_cards


if __name__ == "__main__":
    missing = find_missing_cards("allcards.txt", "card_abilities.txt")
    if not missing:
        print("No missing cards found.")
    else:
        print("Missing cards:")
        for card in sorted(missing):
            print(card)
