# Read all card names from allcards.txt
with open('allcards.txt', 'r') as allcards_file:
    allcards = [line.strip() for line in allcards_file if line.strip()]

# Read card abilities from card_abilities.txt
with open('card_abilities.txt', 'r') as abilities_file:
    abilities = abilities_file.read()

# Find missing cards
missing_cards = [card for card in allcards if card not in abilities]

# Print missing cards to the console
if missing_cards:
    print("Missing cards:")
    for card in missing_cards:
        print(card)
else:
    print("No missing cards found.")