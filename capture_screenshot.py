"""Utilities for capturing a cropped screenshot of the Marvel Snap window."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Optional


SNAP_APP_NAME = "SNAP"
DEFAULT_OUTPUT = Path("screenshot.png")
FOREGROUND_DELAY_SECONDS = 1


def capture_screenshot(output_path: Path | str = DEFAULT_OUTPUT) -> Optional[Path]:
    """
    Activate Marvel Snap and capture an interactive screenshot.

    Parameters
    ----------
    output_path:
        Destination path for the captured screenshot. Defaults to ``screenshot.png`` in
        the current working directory.

    Returns
    -------
    pathlib.Path | None
        The path to the captured screenshot, or ``None`` if the capture failed.
    """
    output_path = Path(output_path)

    # AppleScript command to activate SNAP
    activate_script = '''
    tell application "{app_name}" to activate
    delay {delay} -- Wait for SNAP to come to the foreground
    '''

    # Run the activation script
    subprocess.run(
        [
            "osascript",
            "-e",
            activate_script.format(app_name=SNAP_APP_NAME, delay=FOREGROUND_DELAY_SECONDS),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    # Capture the screenshot interactively
    screenshot_path = Path.home() / "Desktop" / "screenshot.png"
    capture_command = ["screencapture", "-i", str(screenshot_path)]

    print("Please select the SNAP window when the crosshair appears.")
    result = subprocess.run(capture_command, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        print(f"Error capturing screenshot: {result.stderr.strip()}")
        return None

    # Check if the screenshot file exists
    if not screenshot_path.exists():
        print(f"Screenshot file not found at {screenshot_path}")
        return None

    # Move the screenshot to the project directory
    try:
        screenshot_path.replace(output_path)
    except OSError as e:
        print(f"Error moving screenshot: {e}")
        return None

    return output_path

if __name__ == "__main__":
    capture_screenshot()
