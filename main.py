"""CLI entry point for orchestrating the SnapHelp workflow."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter

from dotenv import load_dotenv

from capture_screenshot import capture_screenshot
from divide_screenshot import divide_screenshot
from get_advice import get_strategic_advice
from gpt_interaction import GameState, get_all_descriptions
from read_card_abilities import load_card_abilities

PROJECT_ROOT = Path(__file__).parent


def run_workflow() -> None:
    """Capture the board state, describe it, and request strategic advice."""
    load_dotenv(PROJECT_ROOT / ".env")

    print("Ensure Marvel Snap is running and clearly visible.")
    print("When prompted, use the crosshair to select the Marvel Snap window.")
    input("Press Enter when you're ready to capture the screenshot...")

    print("Capturing screenshot...")
    screenshot_path = capture_screenshot(PROJECT_ROOT / "screenshot.png")
    if screenshot_path is None:
        print("Failed to capture screenshot. Please try again.")
        return

    print(f"Screenshot saved to {screenshot_path.resolve()}")

    print("Dividing screenshot into board sections...")
    try:
        divide_screenshot(screenshot_path, output_dir=PROJECT_ROOT)
    except Exception as exc:
        print(f"Error dividing screenshot: {exc}")
        return

    print("Describing board state with OpenAI...")
    describe_start = perf_counter()
    try:
        game_state: GameState = get_all_descriptions(PROJECT_ROOT, PROJECT_ROOT / "card_abilities.txt")
    except Exception as exc:
        print(f"Error describing board state: {exc}")
        return
    describe_elapsed = perf_counter() - describe_start
    print(f"Descriptions retrieved in {describe_elapsed:.2f} seconds.")

    print("Generating strategic advice...")
    try:
        card_abilities = load_card_abilities(PROJECT_ROOT / "card_abilities.txt")
        advice = get_strategic_advice(game_state, card_abilities, output_path=PROJECT_ROOT / "finalResponse.txt")
        print("\nStrategic Advice:\n")
        print(advice)
    except Exception as exc:
        print(f"Error getting strategic advice: {exc}")


def main() -> None:
    """Entrypoint invoked by the ``python -m`` interface."""
    run_workflow()


if __name__ == "__main__":
    main()
