"""Interact with OpenAI to describe Marvel Snap board regions."""

from __future__ import annotations

import base64
import concurrent.futures
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Mapping, Sequence, Set

from openai import OpenAI

from read_card_abilities import load_card_abilities

SECTION_ORDER: Sequence[str] = (
    "your_cards",
    "location1",
    "location2",
    "location3",
    "energy_turns",
)

PROMPTS: Mapping[str, str] = {
    "your_cards": "List each card in the player's hand with its name. If there are no cards, state that the player has no cards in hand.",
    "location1": "What is the location name? Player cards are on the bottom, opponent cards are on top. For both the player and opponent, list all cards played at the left location with their names and abilities. If there are no cards, state that there are no cards at this location.",
    "location2": "What is the location name? Player cards are on the bottom, opponent cards are on top. For both the player and opponent, list all cards played at the middle location with their names and abilities. If there are no cards, state that there are no cards at this location.",
    "location3": "What is the location name? Player cards are on the bottom, opponent cards are on top. For both the player and opponent, list all cards played at the right location with their names and abilities. If there are no cards, state that there are no cards at this location.",
    "energy_turns": "What is the current energy and turn number?",
}

SECTION_OUTPUTS: Mapping[str, str] = {
    "your_cards": "hand.txt",
    "energy_turns": "energyPower.txt",
    "location1": "location1.txt",
    "location2": "location2.txt",
    "location3": "location3.txt",
}


@dataclass
class GameState:
    """Aggregate of section descriptions and detected cards for prompt building."""

    sections: Dict[str, str]
    referenced_cards: Set[str]

    def to_prompt(self, card_abilities: Mapping[str, str]) -> str:
        """Build a structured prompt that summarises the current game state."""
        sections_text = "\n".join(
            f"{section.capitalize()}:\n{self.sections[section]}"
            for section in SECTION_ORDER
            if section in self.sections
        )

        ability_lines = [
            f"{card}: {card_abilities.get(card, 'Ability unknown')}"
            for card in sorted(self.referenced_cards)
        ]
        ability_text = ""
        if ability_lines:
            ability_text = "Card Ability Reference:\n" + "\n".join(ability_lines)

        prompt_parts = ["Current game state:", sections_text.strip()]
        if ability_text:
            prompt_parts.append("")
            prompt_parts.append(ability_text)
        return "\n".join(part for part in prompt_parts if part).strip()


def get_openai_client() -> OpenAI:
    """Instantiate the OpenAI client using the configured API key."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Please add it to your environment or .env file."
        )
    return OpenAI(api_key=api_key)


def encode_image(image_path: Path) -> str:
    """Return a base64-encoded representation of an image file."""
    data = image_path.read_bytes()
    return base64.b64encode(data).decode("utf-8")


def get_image_description(image_path: Path, section: str, client: OpenAI) -> str:
    """Request a textual description for a cropped board section."""
    base64_image = encode_image(image_path)

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPTS[section]},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}",
                        "detail": "high",
                    },
                },
            ],
        }
    ]

    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=messages,
        max_tokens=2_000,
    )
    return response.choices[0].message.content.strip()


def extract_known_cards(text: str, card_names: Iterable[str]) -> Set[str]:
    """Detect referenced cards based on known card names."""
    lowered = text.lower()
    return {card for card in card_names if card.lower() in lowered}


def get_all_descriptions(
    image_directory: Path | str = Path("."),
    abilities_path: Path | str = Path("card_abilities.txt"),
    client: OpenAI | None = None,
) -> GameState:
    """
    Describe each saved board section and gather referenced card abilities.

    Parameters
    ----------
    image_directory:
        Directory containing the pre-cropped section images.
    abilities_path:
        Path to the ``card_abilities.txt`` reference file.
    client:
        Optional OpenAI client. If omitted, a client is created automatically.

    Returns
    -------
    GameState
        Object encapsulating section descriptions and card references.
    """
    image_directory = Path(image_directory)
    abilities_path = Path(abilities_path)
    client = client or get_openai_client()

    card_abilities = load_card_abilities(abilities_path)
    descriptions: Dict[str, str] = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(SECTION_ORDER)) as executor:
        futures = {
            executor.submit(
                get_image_description,
                image_directory / f"{section}.png",
                section,
                client,
            ): section
            for section in SECTION_ORDER
        }

        for future in concurrent.futures.as_completed(futures):
            section = futures[future]
            try:
                description = future.result()
                descriptions[section] = description
                print(f"Description for {section}:\n{description}\n")

                output_name = SECTION_OUTPUTS.get(section)
                if output_name:
                    (image_directory / output_name).write_text(
                        description,
                        encoding="utf-8",
                    )

            except Exception as exc:
                print(f"{section} generated an exception: {exc}")

    # Ensure deterministic order based on SECTION_ORDER
    ordered_descriptions = {
        section: descriptions[section]
        for section in SECTION_ORDER
        if section in descriptions
    }

    referenced_cards: Set[str] = set()
    for text in ordered_descriptions.values():
        referenced_cards.update(extract_known_cards(text, card_abilities.keys()))

    game_state = GameState(ordered_descriptions, referenced_cards)

    # Persist combined prompt for debugging / transparency
    combined_prompt = game_state.to_prompt(card_abilities)
    (image_directory / "bigprompt.txt").write_text(combined_prompt, encoding="utf-8")

    return game_state


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    get_all_descriptions()
