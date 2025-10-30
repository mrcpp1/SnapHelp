"""Generate strategic advice from a captured Marvel Snap game state."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from openai import OpenAI

from gpt_interaction import GameState, get_all_descriptions, get_openai_client
from read_card_abilities import load_card_abilities

PROMPT_TEMPLATE = """You are a Marvel Snap expert. Given the following game state:

{game_state}

Please analyze the game state and provide strategic advice in the following format:

Analysis:
1. [Analyze the current board state, including played cards and their abilities]
2. [Evaluate the hand cards and their potential impact]
3. [Consider the location effects and how they interact with the cards]
4. [Assess the opponent's likely strategy based on their played cards]

Energy: [current energy]

Recommended Moves:
1. [play/move] [card name] [left/middle/right]. [Card cost]/[Card power] [Card ability description]
2. (Additional moves if applicable)

Explanation: [Explain why these moves are the best options, considering the analysis above, synergies between card abilities, location effects, and the current game state]
"""


def get_strategic_advice(
    game_state: GameState,
    card_abilities: Mapping[str, str],
    client: OpenAI | None = None,
    output_path: Path | str = Path("finalResponse.txt"),
) -> str:
    """
    Request a strategic recommendation from OpenAI based on the game state.

    Parameters
    ----------
    game_state:
        Descriptions of each board section and detected cards.
    card_abilities:
        Mapping of card names to their ability descriptions.
    client:
        Optional OpenAI client. Created automatically when omitted.
    output_path:
        Location where the formatted response should be written.

    Returns
    -------
    str
        The model-generated strategic advice.
    """
    client = client or get_openai_client()
    output_path = Path(output_path)

    prompt_body = PROMPT_TEMPLATE.format(game_state=game_state.to_prompt(card_abilities))
    messages = [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt_body}],
        }
    ]

    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=messages,
        max_tokens=2_000,
    )

    advice = response.choices[0].message.content.strip()
    output_path.write_text(advice, encoding="utf-8")
    return advice


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    abilities = load_card_abilities("card_abilities.txt")
    state = get_all_descriptions()
    print(get_strategic_advice(state, abilities))
