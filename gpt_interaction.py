import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
import concurrent.futures
from read_card_abilities import load_card_abilities

# Load environment variables from .env file
load_dotenv()

# Now create the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_description(image_path, image_type, card_abilities):
    base64_image = encode_image(image_path)

    prompts = {
        "your_cards": "List each card in the player's hand with its name. If there are no cards, state that the player has no cards in hand.",
        "location1": "What is the location name? Players cards are on the bottom, opponents cards are on top. For both the player and opponent, list all cards played at the left location with their names and abilities. If there are no cards, state that there are no cards at this location.",
        "location2": "What is the location name? Players cards are on the bottom, opponents cards are on top. For both the player and opponent, list all cards played at the middle location with their names and abilities. If there are no cards, state that there are no cards at this location.",
        "location3": "What is the location name? Players cards are on the bottom, opponents cards are on top. For both the player and opponent, list all cards played at the right location with their names and abilities. If there are no cards, state that there are no cards at this location.",
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
    response = client.chat.completions.create(model="chatgpt-4o-latest",
                                              messages=messages,
                                              max_tokens=2000)

    return response.choices[0].message.content

def append_abilities(description, card_abilities):
    lines = description.split('\n')
    updated_description = []
    for line in lines:
        card_name = line.strip()
        if card_name in card_abilities:
            power, ability = card_abilities[card_name]
            updated_description.append(f"{card_name}: {power}, {ability}")
        else:
            updated_description.append(f"{card_name}: no power, no ability")
    return '\n'.join(updated_description)

def load_card_abilities(file_path):
    abilities = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                card_name, ability = line.split(':', 1)
                abilities[card_name.strip()] = ability.strip()
    return abilities

def get_image_description_wrapper(args):
    return get_image_description(*args)

def get_all_descriptions():
    sections = ['your_cards', 'location1', 'location2', 'location3', 'energy_turns']
    descriptions = {}
    combined_prompt = "Current game state:\n\n"

    card_abilities = load_card_abilities('card_abilities.txt')

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_section = {executor.submit(get_image_description_wrapper, (f'{section}.png', section, card_abilities)): section for section in sections}
        
        for future in concurrent.futures.as_completed(future_to_section):
            section = future_to_section[future]
            try:
                description = future.result()
                description_with_abilities = append_abilities(description, card_abilities)
                descriptions[section] = description_with_abilities
                print(f"Description for {section}:\n{description_with_abilities}\n")

                # Write descriptions to their respective files
                if section == 'your_cards':
                    with open('hand.txt', 'w') as f:
                        f.write(description_with_abilities)
                elif section == 'energy_turns':
                    with open('energyPower.txt', 'w') as f:
                        f.write(description_with_abilities)
                elif section.startswith('location'):
                    with open(f'{section}.txt', 'w') as f:
                        f.write(description_with_abilities)

                # Add to combined prompt
                combined_prompt += f"{section.capitalize()}:\n{description_with_abilities}\n\n"
            except Exception as exc:
                print(f"{section} generated an exception: {exc}")

    # Write the combined prompt to bigprompt.txt
    with open('bigprompt.txt', 'w') as f:
        f.write(combined_prompt)

    return descriptions

# Load card abilities
card_abilities = load_card_abilities('card_abilities.txt')

if __name__ == "__main__":
    get_all_descriptions()
