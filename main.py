from capture_screenshot import capture_screenshot
from divide_screenshot import divide_screenshot
from get_advice import get_strategic_advice
from gpt_interaction import get_all_descriptions
import time

def main():
    print("Please ensure SNAP is running and visible on the screen.")
    print("When prompted, use the crosshair to select the SNAP window.")
    input("Press Enter when you're ready to capture the screenshot...")

    # Step 1: Capture the screenshot
    print("Attempting to capture screenshot...")
    image_path = capture_screenshot()
    if image_path is None:
        print("Failed to capture screenshot. Please try again.")
        return

    print(f"Screenshot captured successfully: {image_path}")

    # Step 2: Divide the screenshot
    print("Dividing the screenshot...")
    try:
        divide_screenshot(image_path)
    except Exception as e:
        print(f"Error dividing screenshot: {e}")
        return

    # Step 3: Get descriptions from GPT-4 (now multithreaded)
    print("Getting descriptions from GPT-4...")
    start_time = time.time()
    try:
        descriptions = get_all_descriptions()
    except Exception as e:
        print(f"Error getting descriptions: {e}")
        return
    end_time = time.time()
    print(f"Time taken to get all descriptions: {end_time - start_time:.2f} seconds")

    # Step 4: Get strategic advice
    print("Getting strategic advice...")
    try:
        advice = get_strategic_advice(descriptions)
        print("\nStrategic Advice:")
        print(advice)
    except Exception as e:
        print(f"Error getting strategic advice: {e}")

if __name__ == "__main__":
    main()
