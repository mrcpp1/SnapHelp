import subprocess
import os
import time

def capture_screenshot():
    # AppleScript command to activate SNAP
    activate_script = '''
    tell application "SNAP" to activate
    delay 1 -- Wait for SNAP to come to the foreground
    '''

    # Run the activation script
    subprocess.run(['osascript', '-e', activate_script], capture_output=True, text=True)

    # Capture the screenshot interactively
    screenshot_path = os.path.expanduser('~/Desktop/screenshot.png')
    capture_command = ['screencapture', '-i', screenshot_path]
    
    print("Please select the SNAP window when the crosshair appears.")
    result = subprocess.run(capture_command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error capturing screenshot: {result.stderr}")
        return None

    # Check if the screenshot file exists
    if not os.path.exists(screenshot_path):
        print(f"Screenshot file not found at {screenshot_path}")
        return None

    # Move the screenshot to the project directory
    try:
        os.rename(screenshot_path, 'screenshot.png')
    except OSError as e:
        print(f"Error moving screenshot: {e}")
        return None

    return 'screenshot.png'

if __name__ == "__main__":
    capture_screenshot()
