import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
import concurrent.futures

# Load environment variables from .env file
load_dotenv()

# Now create the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_description(image_path, image_type):
    base64_image = encode_image(image_path)

    prompts = {
        "your_cards": "Describe the cards in the player's hand. List each card with its name, cost, power, and a brief description of its ability. If there are no cards, state that the player has no cards in hand.",
        "location1": "Describe the left location. What is its name and effect? Also, list all cards played here, with the opponent's cards on top and the player's cards on the bottom. Include their names, costs, powers, and a brief description of their abilities. If there are no cards, state that there are no cards at this location.",
        "location2": "Describe the middle location. What is its name and effect? Also, list all cards played here, with the opponent's cards on top and the player's cards on the bottom. Include their names, costs, powers, and a brief description of their abilities. If there are no cards, state that there are no cards at this location.",
        "location3": "Describe the right location. What is its name and effect? Also, list all cards played here, with the opponent's cards on top and the player's cards on the bottom. Include their names, costs, powers, and a brief description of their abilities. If there are no cards, state that there are no cards at this location.",
        "energy_turns": "What is the current energy and turn number?"
    }

    # Prepare the message content
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompts[image_type]},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}",
                        "detail": "high"
                    }
                }
            ]
        }
    ]

    # Send the request to the API
    response = client.chat.completions.create(model="chatgpt-4o-latest",  # Changed to gpt-4o
    messages=messages,
    max_tokens=2000)

    return response.choices[0].message.content

def get_image_description_wrapper(args):
    return get_image_description(*args)

def get_all_descriptions():
    sections = ['your_cards', 'location1', 'location2', 'location3', 'energy_turns']
    descriptions = {}
    combined_prompt = "Current game state:\n\n"

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_section = {executor.submit(get_image_description_wrapper, (f'{section}.png', section)): section for section in sections}
        
        for future in concurrent.futures.as_completed(future_to_section):
            section = future_to_section[future]
            try:
                description = future.result()
                descriptions[section] = description
                print(f"Description for {section}:\n{description}\n")

                # Write descriptions to their respective files
                if section == 'your_cards':
                    with open('hand.txt', 'w') as f:
                        f.write(description)
                elif section == 'energy_turns':
                    with open('energyPower.txt', 'w') as f:
                        f.write(description)
                elif section.startswith('location'):
                    with open(f'{section}.txt', 'w') as f:
                        f.write(description)

                # Add to combined prompt
                combined_prompt += f"{section.capitalize()}:\n{description}\n\n"
            except Exception as exc:
                print(f"{section} generated an exception: {exc}")

    # Write the combined prompt to bigprompt.txt
    with open('bigprompt.txt', 'w') as f:
        f.write(combined_prompt)

    return descriptions

if __name__ == "__main__":
    get_all_descriptions()
