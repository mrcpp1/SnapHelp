import os

def load_card_abilities(file_path):
    card_abilities = {}
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                card_name, ability = line.split(':', 1)
                card_abilities[card_name.strip()] = ability.strip()
    
    return card_abilities

if __name__ == "__main__":
    abilities = load_card_abilities('card_abilities.txt')
    for card, ability in abilities.items():
        print(f"{card}: {ability}")