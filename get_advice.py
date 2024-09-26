import os
from openai import OpenAI
from dotenv import load_dotenv
from gpt_interaction import get_all_descriptions

# Load environment variables from .env file
load_dotenv()

# Now create the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_strategic_advice(descriptions):
    combined_text = "\n".join([f"{key}: {value}" for key, value in descriptions.items()])
    final_prompt = f"""You are a Marvel Snap expert. Given the following game state:

{combined_text}

Please analyze the game state and provide strategic advice in the following format:

Analysis:
1. [Analyze the current board state, including played cards and their abilities]
2. [Evaluate the hand cards and their potential impact]
3. [Consider the location effects and how they interact with the cards]
4. [Assess the opponent's likely strategy based on their played cards]

Energy: [current energy]

Recommended Moves:
1. [play/move] [card name] [left/middle/right]. [Card cost]/[Card power] [Card ability description]
2. (Additional moves if applicable)

Explanation: [Explain why these moves are the best options, considering the analysis above, synergies between card abilities, location effects, and the current game state]
"""

    # Prepare the message content
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": final_prompt}
            ]
        }
    ]

    # Send the request to the API
    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=messages,
    max_tokens=2000)

    advice = response.choices[0].message.content

    # Write the advice to finalResponse.txt
    with open('finalResponse.txt', 'w') as f:
        f.write(advice)

    return advice

if __name__ == "__main__":
    # Assume descriptions are already obtained
    descriptions = get_all_descriptions()
    advice = get_strategic_advice(descriptions)
    print("Strategic Advice:")
    print(advice)
