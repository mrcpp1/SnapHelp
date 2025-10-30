# SnapHelp

SnapHelp automates capturing a Marvel Snap board state, slicing it into regions, describing each region with the OpenAI API, and generating strategic advice for the next turn.

## Prerequisites
- macOS (relies on `osascript` and `screencapture`)
- Python 3.10+ recommended
- OpenAI API key with access to `chatgpt-4o-latest`

## Setup
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the sample environment file and add your API key:
   ```bash
   cp .env.example .env
   # edit .env to set OPENAI_API_KEY
   ```

## Usage
1. Launch Marvel Snap so the game window is visible.
2. Run the main workflow:
   ```bash
   python main.py
   ```
3. When prompted, use the crosshair to select the Marvel Snap window.  
   The app will:
   - capture the screenshot,
   - crop it into hand, three locations, and energy/turn overlays,
   - request descriptions for each region from the OpenAI API (see `bigprompt.txt`),
   - produce strategic advice that is saved to `finalResponse.txt`.

Generated screenshots and text summaries are ignored by git (`.gitignore`) so rerunning the workflow will not clutter source control.

## Utilities
- `image_coordinate_finder.py` – GUI helper for finding pixel and relative coordinates in screenshots.
- `cardFInder.py` – checks for cards present in `allcards.txt` that are missing from `card_abilities.txt`.

## Troubleshooting
- Ensure `OPENAI_API_KEY` is set in `.env` before invoking the scripts.
- Adjust the crop ratios in `divide_screenshot.py` if your screen resolution or in-game zoom changes.
