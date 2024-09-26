from PIL import Image

def divide_screenshot(image_path):
    image = Image.open(image_path)
    width, height = image.size

    sections = {}

    # Your cards at the bottom
    sections['your_cards'] = image.crop((int(width * 0), int(height * 0.75), int(width * 1), int(height * 0.890)))

    # Location 1 (left)
    sections['location1'] = image.crop((int(width * 0.160), int(height * 0.215), int(width * 0.385), int(height * 0.760)))

    # Location 2 (middle)
    sections['location2'] = image.crop((int(width * 0.385), int(height * 0.215), int(width * 0.610), int(height * 0.760)))

    # Location 3 (right)
    sections['location3'] = image.crop((int(width * 0.610), int(height * 0.215), int(width * 0.835), int(height * 0.760)))

    # Current energy and turns at the bottom-right corner
    sections['energy_turns'] = image.crop((int(width * 0.420), int(height * 0.895), int(width * 1), int(height * 1)))

    # Save each section as an image file
    for name, img in sections.items():
        img.save(f'{name}.png')

    return sections

if __name__ == "__main__":
    divide_screenshot('screenshot.png')
