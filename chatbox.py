import json
import random

# Load intents
with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)


def get_response(user_message):
    user_message = user_message.lower().strip()

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_message:
                return random.choice(intent["responses"])

    return "Sorry, I didn't understand your question. Please ask something else."